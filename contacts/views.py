from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum, Count, Q, F
import io
import csv
import zipfile
import json
from rest_framework import viewsets
from .models import Customer, Interaction, Task, Deal, Product
from .serializers import CustomerSerializer, InteractionSerializer, TaskSerializer, DealSerializer, ProductSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('-created_at')
    serializer_class = CustomerSerializer


class InteractionViewSet(viewsets.ModelViewSet):
    queryset = Interaction.objects.all().order_by('-date')
    serializer_class = InteractionSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer


class DealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.all().order_by('-created_at')
    serializer_class = DealSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer


def index(request):
    # Dashboard / landing page showing quick stats
    total_clients = Customer.objects.count()
    total_tasks = Task.objects.count()
    total_deals = Deal.objects.count()
    total_products = Product.objects.count()
    return render(request, 'landing.html', {
        'total_clients': total_clients,
        'total_tasks': total_tasks,
        'total_deals': total_deals,
        'total_products': total_products,
    })


def clients_list(request):
    return render(request, 'clients_list.html')


def tasks_list(request):
    return render(request, 'tasks_list.html')


def deals_list(request):
    return render(request, 'deals_list.html')


def products_list(request):
    return render(request, 'products_list.html')
    total_clients = Customer.objects.count()
    total_tasks = Interaction.objects.count()
    total_deals = 0
    total_products = 0
    return render(request, 'landing.html', {
        'total_clients': total_clients,
        'total_tasks': total_tasks,
        'total_deals': total_deals,
        'total_products': total_products,
    })


def download_data(request):
    """Return a ZIP file containing CSV exports for Customers, Tasks, Deals and Products."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Helper to write a queryset to CSV and add to zip
        def add_csv(qs, name):
            if not qs:
                # write empty CSV with header only
                rows = []
                field_names = []
            else:
                field_names = [f.name for f in qs.model._meta.fields]
                rows = []
                for obj in qs:
                    row = []
                    for fn in field_names:
                        val = getattr(obj, fn)
                        # For related fields, stringify
                        try:
                            if hasattr(val, 'isoformat'):
                                val = val.isoformat()
                        except Exception:
                            pass
                        row.append(str(val) if val is not None else '')
                    rows.append(row)

            csv_io = io.StringIO()
            writer = csv.writer(csv_io)
            if field_names:
                writer.writerow(field_names)
            else:
                writer.writerow([])
            for r in rows:
                writer.writerow(r)
            zf.writestr(f"{name}.csv", csv_io.getvalue())

        add_csv(Customer.objects.all(), 'customers')
        add_csv(Task.objects.all(), 'tasks')
        add_csv(Deal.objects.all(), 'deals')
        add_csv(Product.objects.all(), 'products')

    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="crm-data.zip"'
    return response


def reports(request):
    """CRM Reports dashboard with metrics and charts."""
    from datetime import datetime
    
    # Get date filters from query params
    from_date_str = request.GET.get('from_date', '')
    to_date_str = request.GET.get('to_date', '')
    from_date = None
    to_date = None
    
    # Parse dates if provided
    try:
        if from_date_str:
            from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
        if to_date_str:
            to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()
    except ValueError:
        pass
    
    # Build filter kwargs
    filters = {}
    if from_date:
        filters['created_at__date__gte'] = from_date
    if to_date:
        filters['created_at__date__lte'] = to_date
    
    # Overall counts (with date filtering)
    total_clients = Customer.objects.filter(**filters).count()
    total_tasks = Task.objects.filter(**filters).count()
    total_deals = Deal.objects.filter(**filters).count()
    total_products = Product.objects.filter(**filters).count()
    
    # Task breakdown
    task_stats = Task.objects.filter(**filters).values('status').annotate(count=Count('id')).order_by('status')
    task_by_status = {t['status']: t['count'] for t in task_stats}
    
    # Deal metrics
    deal_total_value = Deal.objects.filter(**filters).aggregate(total=Sum('amount'))['total'] or 0
    deal_stats = Deal.objects.filter(**filters).values('status').annotate(count=Count('id'), value=Sum('amount')).order_by('status')
    
    # Customer status distribution
    customer_stats = Customer.objects.filter(**filters).values('status').annotate(count=Count('id')).order_by('status')
    
    # Top products (by name, ordered by creation date)
    top_products = Product.objects.filter(**filters).order_by('-created_at')[:5]
    
    # Recent activity (with date filtering)
    recent_customers = Customer.objects.filter(**filters).order_by('-created_at')[:5]
    recent_tasks = Task.objects.filter(**filters).order_by('-created_at')[:5]
    recent_deals = Deal.objects.filter(**filters).order_by('-created_at')[:5]
    
    # Format data for charts (JSON)
    task_labels = list(task_by_status.keys()) if task_by_status else ['No Data']
    task_counts = list(task_by_status.values()) if task_by_status else [0]
    
    customer_labels = [c['status'] for c in customer_stats]
    customer_counts = [c['count'] for c in customer_stats]
    
    deal_labels = [d['status'] for d in deal_stats]
    deal_values = [float(d['value'] or 0) for d in deal_stats]
    
    context = {
        'total_clients': total_clients,
        'total_tasks': total_tasks,
        'total_deals': total_deals,
        'total_products': total_products,
        'deal_total_value': f"${deal_total_value:,.2f}",
        'task_by_status': json.dumps(task_by_status),
        'task_labels': json.dumps(task_labels),
        'task_counts': json.dumps(task_counts),
        'customer_labels': json.dumps(customer_labels),
        'customer_counts': json.dumps(customer_counts),
        'deal_labels': json.dumps(deal_labels),
        'deal_values': json.dumps(deal_values),
        'top_products': top_products,
        'recent_customers': recent_customers,
        'recent_tasks': recent_tasks,
        'recent_deals': recent_deals,
        'from_date': from_date_str,
        'to_date': to_date_str,
    }
    return render(request, 'reports.html', context)
