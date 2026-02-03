# Financial Period Comparison - Advanced Usage & Examples

## Table of Contents
1. [Code Examples](#code-examples)
2. [Advanced Patterns](#advanced-patterns)
3. [Custom Analysis](#custom-analysis)
4. [Integration Examples](#integration-examples)
5. [Best Practices](#best-practices)

---

## Code Examples

### Example 1: Basic Period Revenue Comparison

```python
from sms import FinancialPeriodComparison
import sqlite3
from datetime import date, timedelta

# Initialize with database connection
conn = sqlite3.connect('database/school_management.db')
period_comp = FinancialPeriodComparison(conn)

# Get revenue for January 2025
jan_revenue = period_comp.get_period_revenue('2025-01-01', '2025-01-31')

print(f"January 2025 Revenue Report:")
print(f"  Total Collected: GHS {jan_revenue['total_revenue']:.2f}")
print(f"  Unique Students: {jan_revenue['unique_students']}")
print(f"  Average Payment: GHS {jan_revenue['avg_payment']:.2f}")
```

**Output:**
```
January 2025 Revenue Report:
  Total Collected: GHS 45,000.00
  Unique Students: 150
  Average Payment: GHS 300.00
```

---

### Example 2: Month-over-Month Comparison

```python
from datetime import date, timedelta

# Get today's date
today = date.today()

# Calculate previous month dates
first_of_month = date(today.year, today.month, 1)
last_of_prev_month = first_of_month - timedelta(days=1)
first_of_prev_month = date(last_of_prev_month.year, last_of_prev_month.month, 1)

# Compare periods
comparison = period_comp.compare_periods(
    first_of_prev_month.strftime('%Y-%m-%d'),
    last_of_prev_month.strftime('%Y-%m-%d'),
    first_of_month.strftime('%Y-%m-%d'),
    today.strftime('%Y-%m-%d')
)

# Display results
p1_rev = comparison['period1']['revenue']
p2_rev = comparison['period2']['revenue']
var = comparison['variance']

print(f"Month-over-Month Comparison")
print(f"{'='*40}")
print(f"Previous Month: GHS {p1_rev['total_revenue']:.2f}")
print(f"Current Month:  GHS {p2_rev['total_revenue']:.2f}")
print(f"Change:         GHS {var['revenue']:+.2f} ({var['revenue_percentage']:+.1f}%)")

if var['revenue_percentage'] > 0:
    print("✓ Collections are improving!")
else:
    print("⚠️ Collections are declining!")
```

**Output:**
```
Month-over-Month Comparison
========================================
Previous Month: GHS 40,000.00
Current Month:  GHS 44,000.00
Change:         GHS +4,000.00 (+10.0%)
✓ Collections are improving!
```

---

### Example 3: Analyzing Collections by Fee Type

```python
# Get fee type breakdown for February 2025
collections = period_comp.get_period_collections_by_type('2025-02-01', '2025-02-28')

print("Collections Breakdown - February 2025")
print(f"{'Fee Type':<20} {'Amount':<15} {'Transactions':<12}")
print("-" * 47)

total_collected = 0
for collection in collections:
    amount = collection['amount']
    print(f"{collection['fee_type']:<20} GHS {amount:>10.2f}  {collection['transactions']:>6}")
    total_collected += amount

print("-" * 47)
print(f"{'TOTAL':<20} GHS {total_collected:>10.2f}")

# Calculate percentages
for collection in collections:
    pct = (collection['amount'] / total_collected * 100) if total_collected > 0 else 0
    print(f"{collection['fee_type']}: {pct:.1f}%")
```

**Output:**
```
Collections Breakdown - February 2025
Fee Type             Amount          Transactions
-----------------------------------------------
School Fee           GHS     35,000  120
Feeding Fee          GHS      8,000  200
Bus Fee              GHS      2,000   50
-----------------------------------------------
TOTAL                GHS     45,000

School Fee: 77.8%
Feeding Fee: 17.8%
Bus Fee: 4.4%
```

---

### Example 4: Identifying Classes with Low Collection Rates

```python
from datetime import date

# Analyze current month by class
today = date.today()
month_start = date(today.year, today.month, 1)

class_collections = period_comp.get_class_wise_collections(
    month_start.strftime('%Y-%m-%d'),
    today.strftime('%Y-%m-%d')
)

# Find classes below 80% collection rate
print("Classes Requiring Attention - February 2025")
print(f"{'Class':<20} {'Rate':<10} {'Collected':<20} {'Status':<15}")
print("-" * 65)

for class_data in class_collections:
    if class_data['collection_rate'] < 80:
        status = "🔴 CRITICAL" if class_data['collection_rate'] < 70 else "🟡 WARNING"
        collected = f"GHS {class_data['total_collected']:.2f}"
        print(f"{class_data['class']:<20} {class_data['collection_rate']:>6.1f}%  {collected:<20} {status}")
```

**Output:**
```
Classes Requiring Attention - February 2025
Class                Rate       Collected            Status         
-----------------------------------------------------------------
Form 2B             70.5%      GHS 2,820.00        🟡 WARNING
Form 3C             65.0%      GHS 2,600.00        🔴 CRITICAL
Form 1D             78.5%      GHS 3,140.00        🟡 WARNING
```

---

### Example 5: Yearly Trend Analysis

```python
from datetime import date, timedelta

# Analyze full year 2024
trends = period_comp.get_monthly_trends('2024-01-01', '2024-12-31')

print("2024 Annual Financial Trends")
print(f"{'Month':<15} {'Collected':<20} {'Arrears':<15} {'Students':<12}")
print("-" * 62)

highest_month = max(trends, key=lambda x: x['total_collected'])
lowest_month = min(trends, key=lambda x: x['total_collected'])

for month_data in trends:
    month = month_data['month']
    collected = month_data['total_collected']
    arrears = month_data['total_arrears']
    students = month_data['students_paid']
    
    print(f"{month:<15} GHS {collected:>13.2f} GHS {arrears:>9.2f}  {students:>10}")

print("-" * 62)
print(f"Highest Collection: {highest_month['month']} - GHS {highest_month['total_collected']:.2f}")
print(f"Lowest Collection:  {lowest_month['month']} - GHS {lowest_month['total_collected']:.2f}")

# Calculate average
avg_collection = sum(m['total_collected'] for m in trends) / len(trends)
print(f"Average Monthly:    GHS {avg_collection:.2f}")
```

**Output:**
```
2024 Annual Financial Trends
Month           Collected            Arrears         Students
--------------------------------------------------------------
2024-01         GHS     40,000.00 GHS   12,000.00       150
2024-02         GHS     38,500.00 GHS   13,200.00       148
...
2024-12         GHS     42,000.00 GHS    8,500.00       155
--------------------------------------------------------------
Highest Collection: 2024-06 - GHS 48,500.00
Lowest Collection:  2024-02 - GHS 38,500.00
Average Monthly:    GHS 42,375.00
```

---

## Advanced Patterns

### Pattern 1: Automated Monthly Report Generation

```python
def generate_monthly_report():
    """Generate automatic monthly comparison report"""
    from datetime import date, timedelta
    import sqlite3
    from sms import FinancialPeriodComparison
    
    conn = sqlite3.connect('database/school_management.db')
    period_comp = FinancialPeriodComparison(conn)
    
    # Calculate periods
    today = date.today()
    first_of_month = date(today.year, today.month, 1)
    last_of_prev = first_of_month - timedelta(days=1)
    first_of_prev = date(last_of_prev.year, last_of_prev.month, 1)
    
    # Get comparison
    comparison = period_comp.compare_periods(
        first_of_prev.strftime('%Y-%m-%d'),
        last_of_prev.strftime('%Y-%m-%d'),
        first_of_month.strftime('%Y-%m-%d'),
        today.strftime('%Y-%m-%d')
    )
    
    # Generate report data
    report = {
        'period': f"{first_of_month.strftime('%B %Y')}",
        'revenue_variance': comparison['variance']['revenue'],
        'revenue_variance_pct': comparison['variance']['revenue_percentage'],
        'arrears_variance': comparison['variance']['arrears'],
        'arrears_variance_pct': comparison['variance']['arrears_percentage'],
        'current_students': comparison['period2']['revenue']['unique_students'],
        'timestamp': today.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return report

# Usage
monthly_report = generate_monthly_report()
print(f"Report for {monthly_report['period']}")
print(f"Revenue Change: {monthly_report['revenue_variance_pct']:+.1f}%")
print(f"Arrears Change: {monthly_report['arrears_variance_pct']:+.1f}%")
```

---

### Pattern 2: Comparative Analysis with Thresholds

```python
def analyze_collection_health():
    """Analyze overall collection health with thresholds"""
    from datetime import date
    import sqlite3
    from sms import FinancialPeriodComparison
    
    conn = sqlite3.connect('database/school_management.db')
    period_comp = FinancialPeriodComparison(conn)
    
    # Define thresholds
    EXCELLENT_RATE = 90
    GOOD_RATE = 80
    ACCEPTABLE_RATE = 70
    
    # Get current month data
    today = date.today()
    month_start = date(today.year, today.month, 1)
    
    class_data = period_comp.get_class_wise_collections(
        month_start.strftime('%Y-%m-%d'),
        today.strftime('%Y-%m-%d')
    )
    
    # Categorize classes
    results = {
        'excellent': [],
        'good': [],
        'acceptable': [],
        'critical': []
    }
    
    for class_info in class_data:
        rate = class_info['collection_rate']
        if rate >= EXCELLENT_RATE:
            results['excellent'].append(class_info)
        elif rate >= GOOD_RATE:
            results['good'].append(class_info)
        elif rate >= ACCEPTABLE_RATE:
            results['acceptable'].append(class_info)
        else:
            results['critical'].append(class_info)
    
    return results

# Usage
health = analyze_collection_health()
print(f"🟢 Excellent ({len(health['excellent'])} classes):")
for cls in health['excellent']:
    print(f"  - {cls['class']}: {cls['collection_rate']:.1f}%")

print(f"🔴 Critical ({len(health['critical'])} classes):")
for cls in health['critical']:
    print(f"  - {cls['class']}: {cls['collection_rate']:.1f}%")
```

---

### Pattern 3: Trend Prediction (Simple)

```python
def predict_quarterly_collections():
    """Simple prediction based on recent trends"""
    from datetime import date, timedelta
    import sqlite3
    from sms import FinancialPeriodComparison
    
    conn = sqlite3.connect('database/school_management.db')
    period_comp = FinancialPeriodComparison(conn)
    
    # Get last 3 months of data
    today = date.today()
    start_date = today - timedelta(days=90)
    
    trends = period_comp.get_monthly_trends(
        start_date.strftime('%Y-%m-%d'),
        today.strftime('%Y-%m-%d')
    )
    
    if len(trends) < 3:
        return None
    
    # Calculate average growth
    collections = [m['total_collected'] for m in trends]
    growth_rates = [
        (collections[i] - collections[i-1]) / collections[i-1] 
        for i in range(1, len(collections))
    ]
    avg_growth = sum(growth_rates) / len(growth_rates)
    
    # Project next month
    last_month_collection = collections[-1]
    projected_collection = last_month_collection * (1 + avg_growth)
    
    return {
        'current_trend': avg_growth * 100,
        'projected_next_month': projected_collection,
        'confidence': 'Low' if len(trends) < 6 else 'Medium'
    }

# Usage
forecast = predict_quarterly_collections()
if forecast:
    print(f"Trend: {forecast['current_trend']:+.1f}% per month")
    print(f"Projected Next Month: GHS {forecast['projected_next_month']:.2f}")
    print(f"Confidence: {forecast['confidence']}")
```

---

## Custom Analysis

### Analysis 1: Payment Delay Impact

```python
def analyze_payment_delays():
    """Analyze impact of payment delays on cash flow"""
    from datetime import date
    import sqlite3
    from sms import FinancialPeriodComparison
    
    conn = sqlite3.connect('database/school_management.db')
    period_comp = FinancialPeriodComparison(conn)
    
    today = date.today()
    
    # Get payment status distribution
    month_start = date(today.year, today.month, 1)
    status_dist = period_comp.get_payment_status_distribution(
        month_start.strftime('%Y-%m-%d'),
        today.strftime('%Y-%m-%d')
    )
    
    print("Payment Status Analysis")
    print(f"{'Status':<15} {'Count':<10} {'Amount Due':<20} {'Amount Paid':<20}")
    print("-" * 65)
    
    total_due = 0
    total_paid = 0
    
    for status in status_dist:
        print(f"{status['status']:<15} {status['count']:<10} GHS {status['amount_due']:>15.2f} GHS {status['amount_paid']:>15.2f}")
        total_due += status['amount_due']
        total_paid += status['amount_paid']
    
    print("-" * 65)
    collection_rate = (total_paid / total_due * 100) if total_due > 0 else 0
    delayed_amount = total_due - total_paid
    
    print(f"Overall Collection Rate: {collection_rate:.1f}%")
    print(f"Delayed Payments: GHS {delayed_amount:.2f}")
    print(f"Impact: Lost {100-collection_rate:.1f}% of expected cash flow")

analyze_payment_delays()
```

---

### Analysis 2: Class Performance Scorecard

```python
def create_class_scorecard():
    """Create comprehensive class performance scorecard"""
    from datetime import date
    import sqlite3
    from sms import FinancialPeriodComparison
    
    conn = sqlite3.connect('database/school_management.db')
    period_comp = FinancialPeriodComparison(conn)
    
    today = date.today()
    month_start = date(today.year, today.month, 1)
    
    class_data = period_comp.get_class_wise_collections(
        month_start.strftime('%Y-%m-%d'),
        today.strftime('%Y-%m-%d')
    )
    
    # Calculate rankings and scores
    for i, class_info in enumerate(sorted(class_data, key=lambda x: x['collection_rate'], reverse=True), 1):
        score = class_info['collection_rate']
        
        if score >= 95:
            grade = 'A+'
            status = '⭐'
        elif score >= 90:
            grade = 'A'
            status = '⭐'
        elif score >= 85:
            grade = 'B'
            status = '👍'
        elif score >= 80:
            grade = 'C'
            status = '⚠️'
        elif score >= 70:
            grade = 'D'
            status = '🔴'
        else:
            grade = 'F'
            status = '❌'
        
        print(f"{i}. {class_info['class']:<15} {grade} ({score:.1f}%) {status}")

create_class_scorecard()
```

---

## Integration Examples

### Integration 1: Email Report Generation

```python
def email_period_comparison_report(recipient_email):
    """Generate and email period comparison report"""
    from datetime import date, timedelta
    import sqlite3
    from sms import FinancialPeriodComparison
    
    conn = sqlite3.connect('database/school_management.db')
    period_comp = FinancialPeriodComparison(conn)
    
    # Get data
    today = date.today()
    month_start = date(today.year, today.month, 1)
    prev_month_end = month_start - timedelta(days=1)
    prev_month_start = date(prev_month_end.year, prev_month_end.month, 1)
    
    comparison = period_comp.compare_periods(
        prev_month_start.strftime('%Y-%m-%d'),
        prev_month_end.strftime('%Y-%m-%d'),
        month_start.strftime('%Y-%m-%d'),
        today.strftime('%Y-%m-%d')
    )
    
    # Format email body
    email_body = f"""
    Financial Period Comparison Report
    Generated: {today}
    
    ═══════════════════════════════════
    
    Month-over-Month Comparison:
    
    Previous Month Total: GHS {comparison['period1']['revenue']['total_revenue']:.2f}
    Current Month Total:  GHS {comparison['period2']['revenue']['total_revenue']:.2f}
    
    Change: {comparison['variance']['revenue_percentage']:+.1f}%
    Amount: GHS {comparison['variance']['revenue']:+.2f}
    
    Arrears Change: {comparison['variance']['arrears_percentage']:+.1f}%
    
    Current Students Paying: {comparison['period2']['revenue']['unique_students']}
    
    ═══════════════════════════════════
    
    Please review the attached dashboard for detailed analysis.
    """
    
    # In real implementation, send via SMTP
    # send_email(recipient_email, "Financial Report", email_body)
    
    return email_body

# Usage
report = email_period_comparison_report('admin@school.com')
print(report)
```

---

## Best Practices

### 1. Regular Monitoring Schedule

```python
# Recommended monitoring frequency
monitoring_schedule = {
    'daily': ['Quick cash position check', 'Review period trends'],
    'weekly': ['Class collection status', 'Arrears update'],
    'monthly': ['Full period comparison', 'Trend analysis', 'Class scorecard'],
    'quarterly': ['Trend forecasting', 'Policy effectiveness review'],
    'annually': ['Year-over-year analysis', 'Strategic planning']
}

# Set calendar reminders for each
def setup_monitoring_alerts():
    """Setup automated monitoring schedule"""
    # Implement with your scheduler
    pass
```

### 2. Data Validation Before Analysis

```python
def validate_period_data(start_date, end_date):
    """Validate data quality before analysis"""
    import sqlite3
    
    conn = sqlite3.connect('database/school_management.db')
    cursor = conn.cursor()
    
    # Check for records
    cursor.execute(
        "SELECT COUNT(*) FROM fees WHERE payment_date BETWEEN ? AND ?",
        (start_date, end_date)
    )
    record_count = cursor.fetchone()[0]
    
    # Check for null values
    cursor.execute(
        "SELECT COUNT(*) FROM fees WHERE amount_due IS NULL OR amount_paid IS NULL"
    )
    null_count = cursor.fetchone()[0]
    
    return {
        'has_data': record_count > 0,
        'record_count': record_count,
        'null_issues': null_count,
        'is_valid': record_count > 0 and null_count == 0
    }
```

### 3. Handling Edge Cases

```python
def safe_compare_periods(p1_start, p1_end, p2_start, p2_end):
    """Safely compare periods with error handling"""
    import sqlite3
    from sms import FinancialPeriodComparison
    
    try:
        conn = sqlite3.connect('database/school_management.db')
        period_comp = FinancialPeriodComparison(conn)
        
        # Validate dates
        if p1_start > p1_end or p2_start > p2_end:
            raise ValueError("Invalid date ranges")
        
        # Perform comparison
        result = period_comp.compare_periods(p1_start, p1_end, p2_start, p2_end)
        
        # Validate result
        if not result:
            return {'error': 'No data available for comparison'}
        
        return {'success': True, 'data': result}
        
    except Exception as e:
        return {'error': str(e), 'success': False}
```

---

## Summary of Examples

| Example | Use Case | Complexity |
|---------|----------|-----------|
| Basic Revenue | Quick revenue check | ⭐ |
| Month-over-Month | Monthly performance | ⭐⭐ |
| Fee Type Analysis | Revenue breakdown | ⭐⭐ |
| Class Analysis | Performance by class | ⭐⭐ |
| Yearly Trends | Long-term analysis | ⭐⭐⭐ |
| Automated Reports | Email generation | ⭐⭐⭐ |
| Health Analysis | Collection status | ⭐⭐⭐ |
| Forecasting | Trend prediction | ⭐⭐⭐⭐ |

---

## Quick Reference

```python
# Most commonly used methods
period_comp = FinancialPeriodComparison(conn)

# Get period revenue
revenue = period_comp.get_period_revenue(start, end)

# Compare two periods
comparison = period_comp.compare_periods(p1_start, p1_end, p2_start, p2_end)

# Get monthly trends
trends = period_comp.get_monthly_trends(start, end)

# Class-wise collections
classes = period_comp.get_class_wise_collections(start, end)
```

---

*For more information, see PERIOD_COMPARISON_FINANCIAL_FEATURES.md*
