import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_category_pie_chart(df, trans_type='expense'):
    '''Create a pie chart for spending by category'''
    filtered = df[df['type'] == trans_type]
    if filtered.empty:
        return None
    
    category_totals = filtered.groupby('category')['amount'].sum().reset_index()
    
    fig = px.pie(
        category_totals,
        values='amount',
        names='category',
        title=f'{trans_type.capitalize()} by Category'
    )
    return fig

def create_monthly_trend_chart(df):
    '''Create a line chart showing monthly trends'''
    if df.empty:
        return None
    
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M').astype(str)

    monthly = df.groupby(['month', 'type'])['amount'].sum().reset_index()

    fig = px.line(
        monthly,
        x='month',
        y='amount',
        color='type',
        title='Monthly Income vs Expenses',
        markers=True
    )

    # Format x-axis to show month names
    fig.update_xaxes(
        dtick="M1",  # Show every month
        tickformat="%b %Y"  # Format as "Jan 2025", "Feb 2025", etc.
    )

    return fig

def create_category_bar_chart(df, trans_type='expense', top_n=10):
    '''Create a bar chart for top categories'''
    filtered = df[df['type'] == trans_type]
    if filtered.empty:
        return None
    
    category_totals = filtered.groupby('category')['amount'].sum().sort_values(ascending=False).head(top_n)
    
    fig = go.Figure(data=[
        go.Bar(x=category_totals.index, y=category_totals.values)
    ])
    fig.update_layout(
        title=f'Top {top_n} {trans_type.capitalize()} Categories',
        xaxis_title='Category',
        yaxis_title='Amount'
    )
    return fig