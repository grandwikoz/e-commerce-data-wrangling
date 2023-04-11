#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlite3
import pandas as pd
import seaborn as sns
from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# In[2]:


#reading all database and store them in each variable
con = sqlite3.connect('olist.db')
order_items = pd.read_sql('SELECT * from olist_order_items_dataset', con)
customers = pd.read_sql('SELECT * from olist_order_customer_dataset', con)
geolocation = pd.read_sql('SELECT * from olist_geolocation_dataset', con)
order_payments = pd.read_sql('SELECT * from olist_order_payments_dataset', con)
order_reviews = pd.read_sql('SELECT * from olist_order_reviews_dataset', con)
orders = pd.read_sql('SELECT * from olist_order_dataset', con)
products = pd.read_sql('SELECT * from olist_products_dataset', con)
sellers = pd.read_sql('SELECT * from olist_sellers_dataset', con)


# In[3]:


#creating a Class with three functions to clean data
@dataclass
class Cleaning:
    df : pd.DataFrame
        
    #Using upper and lower boundaries to define outliers and change their value using median
    def impute_outliers(self):
        columns = list(self.df.columns.values)
        for column in columns:
            try:
                q3 = self.df[column].quantile(q=0.75)
                q1 = self.df[column].quantile(q=0.25)
                iqr = q3 - q1
                upper_limit = q3 + iqr*1.5
                lower_limit = q1 - iqr*1.5
                median = self.df[column].median()
                self.df.loc[self.df[column]>upper_limit, column] = median
                self.df.loc[self.df[column]<lower_limit, column] = median
            except:
                pass
            
    #Change non-float null into 'unknown' and float null into median
    def impute_missing(self):
        columns = list(self.df.columns.values)
        for column in columns:
            try:
                if self.df[column].dtypes.name == 'float64':
                    median = self.df[column].median()
                    self.df[column] = self.df[column].fillna(median)
                else:
                    self.df[column] = self.df[column].fillna('unknown')
            except:
                pass
    
    #Drop duplicates
    def del_duplicate(self):
        self.df = self.df.drop_duplicates(keep='first')


# In[4]:


#cleaning order_items
clean_order_items = Cleaning(order_items)
clean_order_items.impute_outliers()
clean_order_items.impute_missing()
clean_order_items.del_duplicate()
order_items.describe()


# In[5]:


order_items.isnull().sum()


# In[8]:


#cleaning orders
clean_orders = Cleaning(orders)
clean_orders.impute_outliers()
clean_orders.impute_missing()
clean_orders.del_duplicate()
orders.describe()


# In[9]:


orders.isnull().sum()


# In[10]:


#cleaning products
clean_products = Cleaning(products)
clean_products.impute_outliers()
clean_products.impute_missing()
clean_products.del_duplicate()
products.describe()


# In[11]:


products.isnull().sum()


# In[12]:


#cleaning order_payments
clean_order_payments = Cleaning(order_payments)
clean_order_payments.impute_outliers()
clean_order_payments.impute_missing()
clean_order_payments.del_duplicate()
order_payments.describe()


# In[13]:


order_payments.isnull().sum()


# In[14]:


#cleaning order_reviews
clean_order_order_reviews = Cleaning(order_reviews)
clean_order_order_reviews.impute_outliers()
clean_order_order_reviews.impute_missing()
clean_order_order_reviews.del_duplicate()
order_reviews.describe()


# In[15]:


order_reviews.isnull().sum()


# In[16]:


#cleaning sellers
clean_order_sellers = Cleaning(sellers)
clean_order_sellers.impute_outliers()
clean_order_sellers.impute_missing()
clean_order_sellers.del_duplicate()
sellers.describe()


# In[17]:


sellers.isnull().sum()


# In[18]:


#cleaning customers
clean_customers = Cleaning(customers)
clean_customers.impute_outliers()
clean_customers.impute_missing()
clean_customers.del_duplicate()
customers.describe()


# In[19]:


customers.isnull().sum()


# In[20]:


#cleaning geolocation
clean_geolocation = Cleaning(geolocation)
clean_geolocation.impute_outliers()
clean_geolocation.impute_missing()
clean_geolocation.del_duplicate()
geolocation.describe()


# In[21]:


geolocation.isnull().sum()


# In[22]:


products.head()


# In[24]:


order_items.head()


# In[25]:


orders.head()


# In[26]:


#joining order_items, products, order_reviews, and order payments to create order_total as a total database for further analysis
order_total = order_items.merge(orders, on='order_id').merge(products, on='product_id').merge(order_reviews, on='order_id').merge(order_payments, on='order_id')


# In[27]:


order_total.head()


# In[28]:


order_total.info()


# In[29]:


order_total = order_total.drop(['index', 'index_x', 'index_y'], axis=1)


# In[30]:


order_total.info()


# In[31]:


order_total.head()


# In[32]:


#converting data columns into datetype values

to_date = list(order_total.columns[[4,9,10,11,12,13,26,27]].values)
order_total[to_date] = order_total[to_date].apply(pd.to_datetime, errors='coerce')


# In[33]:


order_total.info()


# In[34]:


order_total = order_total.dropna()


# In[35]:


order_total.info()


# In[36]:


#Adding some order properties regarding time dimension
order_total['order_purchase_hr'] = order_total['order_purchase_timestamp'].dt.hour
order_total['order_purchase_day'] = order_total['order_purchase_timestamp'].dt.day
order_total['order_purchase_month'] = order_total['order_purchase_timestamp'].dt.month
order_total['order_purchase_year'] = order_total['order_purchase_timestamp'].dt.year
order_total['order_purchase_dayofweek'] = order_total['order_purchase_timestamp'].dt.dayofweek
order_total['order_delivery_time'] = ((order_total['order_delivered_customer_date'] - order_total['order_purchase_timestamp'])/np.timedelta64(1, 'D')).astype(int)
order_total['order_estimation_time_gap'] = ((order_total['order_delivered_customer_date'] - order_total['order_estimated_delivery_date'])/np.timedelta64(1, 'D')).astype(int)
order_total['order_process_time'] = ((order_total['order_delivered_carrier_date'] - order_total['order_purchase_timestamp'])/np.timedelta64(1, 'D')).astype(int)
order_total['order_carrier_time'] = ((order_total['order_delivered_customer_date'] - order_total['order_delivered_carrier_date'])/np.timedelta64(1, 'D')).astype(int)
order_total['review_process_time'] = ((order_total['review_answer_timestamp'] - order_total['review_creation_date'])/np.timedelta64(1, 'D')).astype(int)


# In[37]:


order_total.head()


# In[38]:


order_total.head()


# In[39]:


order_total[order_total['payment_type']=='not_defined']


# In[40]:


order_total.info()


# In[61]:


#show top five items based on total sales
top_items = order_total[['product_id', 'product_category_name', 'price']].groupby(['product_id', 'product_category_name'], as_index=False).sum().sort_values('price', ascending=False).head()
top_items.index = range(0,5,1)
top_items.rename(columns={'price':'sales'}, inplace=True)
top_items


# In[62]:


#create a barplot of sales of top five items
sns.barplot(data=top_items, x='sales', y='product_id')
plt.show()


# In[59]:


#create a barplot of top five categories based on sales
top_cat = order_total[['product_category_name', 'price']].groupby(['product_category_name'], as_index=False).sum().sort_values('price', ascending=False).head()
top_cat.index = range(0,5,1)
top_cat.rename(columns={'price':'sales'}, inplace=True)
top_cat


# In[60]:


#create a barplot of top five categories based on sales
sns.barplot(data=top_cat, x='sales', y='product_category_name')


# In[65]:


#showing total products based on number of photos they have
top_based_photos_qty = order_total[['product_photos_qty', 'product_id']].groupby(['product_photos_qty'], as_index=False).count().sort_values('product_id', ascending=False)
top_based_photos_qty.rename(columns={'product_id':'number_of_products'}, inplace=True)
top_based_photos_qty


# In[66]:


sns.barplot(data=top_based_photos_qty, x='product_photos_qty', y='number_of_products')
plt.show()


# In[44]:


order_total.pivot_table(values='product_id', index='product_category_name', columns='product_photos_qty', aggfunc='count', fill_value=0,  margins=True).sort_values('All', ascending=False)


# In[67]:


#based on order_total, create an order_origin to add seller and customer identification
order_origin = order_total[['order_id','product_id', 'product_category_name', 'customer_id', 'seller_id', 'price', 'freight_value', 'review_score', 'order_purchase_hr', 'order_purchase_day', 'order_purchase_month', 'order_purchase_year', 'order_purchase_dayofweek', 'order_delivery_time', 'order_estimation_time_gap', 'order_process_time', 'order_carrier_time', 'review_process_time']].merge(customers[['customer_id', 'customer_city', 'customer_state']], on='customer_id').merge(sellers[['seller_id', 'seller_city', 'seller_state']], on='seller_id')
order_origin.head()


# In[68]:


order_origin.pivot_table(values='price', index='product_category_name', columns='customer_state', aggfunc='sum', fill_value=0, margins=True).sort_values('All', ascending=False)


# In[71]:


#show total sales based on seller state and categories
order_origin_sales = pd.DataFrame(order_origin.groupby(['seller_state', 'product_category_name'], as_index=False)['price'].sum())
order_origin_sales.rename(columns={'price':'total_sales', 'seller_state':'state'}, inplace=True)
order_origin_sales


# In[70]:


#show total purchase based on customer state and categories
order_origin_purchase = pd.DataFrame(order_origin.groupby(['customer_state', 'product_category_name'], as_index=False)['price'].sum())
order_origin_purchase.rename(columns={'price':'total_purchase', 'customer_state':'state'}, inplace=True)
order_origin_purchase


# In[72]:


#create a list of top five category sales
top_cat_list = list(top_cat['product_category_name'].values)
top_cat_list


# In[73]:


#create a list of top five state of sales with corresponding states
state_list = list(order_origin['seller_state'].values) + list(order_origin['customer_state'].values)
state_list = pd.DataFrame({'state': list(set(state_list))})
state_list.head()


# In[74]:


#show sales origin (seller)
sales_origin = order_origin[['seller_state', 'price']].groupby(['seller_state'], as_index=False).sum().sort_values('price', ascending=False)
sales_origin.rename(columns={'price':'total_sales', 'seller_state':'state'}, inplace=True)
sales_origin.head()


# In[75]:


#show purchase origin (customer)
purchase_origin = order_origin[['customer_state', 'price']].groupby(['customer_state'], as_index=False).sum().sort_values('price', ascending=False)
purchase_origin.rename(columns={'price':'total_purchase', 'customer_state':'state'}, inplace=True)
purchase_origin.head()


# In[76]:


#show total sales and purchase from top five states
order_origin_top_state = sales_origin.merge(purchase_origin, on='state', how='outer').fillna(0).head(5)
order_origin_top_state


# In[189]:


#create a barplot showing difference between sales and purchase from top five states
order_origin_top_state.plot(x='state', kind='bar', figsize=(7,4), grid=False)
plt.xlabel("States")
plt.ylabel("Amount")
plt.title("Sales-Purchase Comparion in Top Five States")
plt.ylim(300000,7000000)
plt.legend()
plt.show()


# In[78]:


top_state_list = list(order_origin_top_state['state'].values)
top_state_list


# In[80]:


#create a pivot showing top sales and purchase broken down into state and category
order_origin_top_cat = order_origin_sales.merge(order_origin_purchase, on=['state', 'product_category_name'], how='outer').fillna(0)
order_origin_top_cat = order_origin_top_cat.loc[(order_origin_top_cat['state'].isin(top_state_list)) & (order_origin_top_cat['product_category_name'].isin(top_cat_list))].reset_index().drop('index', axis=1)
order_origin_top_cat


# In[81]:


min(order_origin_top_cat['total_purchase'].min(), order_origin_top_cat['total_sales'].min())


# In[82]:


top_state_list


# In[84]:


#creating plots showing sales comparison of top five categories in top five states
sns.set_style('darkgrid')
fig, axes = plt.subplots(5, 1, figsize=(3,15))
fig.suptitle('Sales Comparions for Top 5 States and Top 5 Categories')



for i, state in enumerate(top_state_list):
    sns.barplot(data=order_origin_top_cat[order_origin_top_cat['state']==state], x ='total_sales', y = 'product_category_name',
                    palette='plasma',
                    lw=3, ax=axes[i])
    xmin = order_origin_top_cat['total_sales'].min()
    xmax = order_origin_top_cat['total_sales'].max()
    axes[i].set_title(str(state))
    axes[i].set_xlim(xmin,xmax)
plt.subplots_adjust(hspace = 0.8)


# In[85]:


#creating plots showing purchase comparison of top five categories in top five states
sns.set_style('darkgrid')
fig, axes = plt.subplots(5, 1, figsize=(3,15))
fig.suptitle('Purchase Comparions for Top 5 States and Top 5 Categories')


for i, state in enumerate(top_state_list):
    sns.barplot(data=order_origin_top_cat[order_origin_top_cat['state']==state], x ='total_purchase', y = 'product_category_name',
                    palette='plasma',
                    lw=3, ax=axes[i])
    xmin = order_origin_top_cat['total_purchase'].min()
    xmax = order_origin_top_cat['total_purchase'].max()
    axes[i].set_title(str(state))
    axes[i].set_xlim(xmin,xmax)
plt.subplots_adjust(hspace = 0.8)


# In[106]:


sns.set_style('white')
fig, axes = plt.subplots(5, 1, figsize=(3,15))
fig.suptitle('Sales-Purchase Comparions for Top 5 States and Top 5 Categories')


for i, state in enumerate(top_state_list):
    ax = plt.subplots
    ax = sns.barplot(data=order_origin_top_cat[order_origin_top_cat['state']==state], x ='total_sales', y = 'product_category_name',
                    lw=3, ax=axes[i], color='b', label='Sales')
    ax = sns.barplot(data=order_origin_top_cat[order_origin_top_cat['state']==state], x ='total_purchase', y = 'product_category_name',
                    lw=3, ax=axes[i], color='r', label='Purchase')
    xmin = min(order_origin_top_cat['total_purchase'].min(), order_origin_top_cat['total_sales'].min())
    xmax = max(order_origin_top_cat['total_purchase'].max(), order_origin_top_cat['total_sales'].max())
    axes[i].set_title(str(state))
    axes[i].set_xlim(xmin,xmax)
    ax.set(xlabel='amount', ylabel="product")
    plt.legend(bbox_to_anchor=(1, 1)) #create legend
plt.subplots_adjust(hspace = 0.8)


# In[107]:


order_total.head()


# In[108]:


order_time_hourly = pd.DataFrame(order_total.groupby(['order_purchase_hr', 'order_purchase_year'])['order_id'].count())
order_time_hourly.head()


# In[109]:


#create a lineplot showing sales based on hour of the day
sns.set_style('darkgrid') # style 
sns.set(rc={'figure.figsize':(14,8)}) #mengatur ukuran gambar

ax = sns.lineplot(data=order_time_hourly, x ='order_purchase_hr', y = 'order_id',
                  hue='order_purchase_year', palette='Set2',
                  legend='full', lw=3) #membuat lineplot

ax.xaxis.set_major_locator(ticker.MultipleLocator(1)) #mengatur sumbu x bertambah 1
plt.title('Hourly Sales Frequency')
plt.legend(bbox_to_anchor=(1, 1)) #membuat legend
plt.ylabel('Sales')
plt.xlabel('Hour')
plt.show()


# In[110]:


order_time_daily = pd.DataFrame(order_total.groupby(['order_purchase_dayofweek', 'order_purchase_year'])['order_id'].count())
order_time_daily.head()


# In[111]:


#create a lineplot showing sales based on day of the week
sns.set_style('darkgrid') # style 
sns.set(rc={'figure.figsize':(14,8)}) #mengatur ukuran gambar

ax = sns.lineplot(data=order_time_daily, x ='order_purchase_dayofweek', y = 'order_id',
                  hue='order_purchase_year', palette='Set2',
                  legend='full', lw=3) #membuat lineplot

ax.xaxis.set_major_locator(ticker.MultipleLocator(1)) #mengatur sumbu x bertambah 1
plt.title('Daily Sales Frequency')
plt.legend(bbox_to_anchor=(1, 1)) #membuat legend
plt.ylabel('Sales')
plt.xlabel('Day')
plt.show()


# In[112]:


order_time_monthly = pd.DataFrame(order_total.groupby(['order_purchase_month', 'order_purchase_year'])['order_id'].count())
order_time_monthly.head()


# In[113]:


#create a lineplot showing sales based on month
sns.set_style('darkgrid') # style 
sns.set(rc={'figure.figsize':(14,8)}) #mengatur ukuran gambar

ax = sns.lineplot(data=order_time_monthly, x ='order_purchase_month', y = 'order_id',
                  hue='order_purchase_year', palette='Set2',
                  legend='full', lw=3) #membuat lineplot

ax.xaxis.set_major_locator(ticker.MultipleLocator(1)) #mengatur sumbu x bertambah 1
plt.title('Monthly Sales Frequency')
plt.legend(bbox_to_anchor=(1, 1)) #membuat legend
plt.ylabel('Sales')
plt.xlabel('Month')
plt.show()


# In[114]:


order_origin.head()


# In[115]:


#create a pivot of sales hourly frequency based on customer state and category
order_hr_origin_cat = pd.DataFrame(order_origin.groupby(['order_purchase_hr', 'customer_state', 'product_category_name'], as_index=False)['order_id'].count())
order_hr_origin_cat


# In[117]:


order_hr_top_origin_cat = order_hr_origin_cat.loc[(order_hr_origin_cat['customer_state'].isin(top_state_list) & order_hr_origin_cat['product_category_name'].isin(top_cat_list))].reset_index().drop('index', axis=1)
order_hr_top_origin_cat.sort_values('order_id', ascending=False)


# In[191]:


#showing lineplot of top states and top categrories based on hour frequecncy
sns.set_style('darkgrid') # style 
sns.set(rc={'figure.figsize':(10,5)}) #mengatur ukuran gambar

ax = sns.lineplot(data=order_hr_top_origin_cat, x ='order_purchase_hr', y = 'order_id',
                  hue='customer_state', palette='Set2',
                  legend='full', lw=3) #membuat lineplot
sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
ax.xaxis.set_major_locator(ticker.MultipleLocator(1)) #mengatur sumbu x bertambah 1
plt.title('Hourly/Origin Sales Frequency')
# plt.legend(bbox_to_anchor=(1, 1)) #membuat legend
plt.ylabel('Sales')
plt.xlabel('Hour')
plt.show()

ax = sns.lineplot(data=order_hr_top_origin_cat, x ='order_purchase_hr', y = 'order_id',
                  hue='product_category_name', palette='Set2',
                  legend='full', lw=3) #membuat lineplot
sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
ax.xaxis.set_major_locator(ticker.MultipleLocator(1)) #mengatur sumbu x bertambah 1
plt.title('Hourly/Product Sales Frequency')
# plt.legend(bbox_to_anchor=(1, 1)) #membuat legend
plt.ylabel('Sales')
plt.xlabel('Hour')
plt.show()


# In[118]:


#create a pivot of sales daily  frequency based on customer state and category
order_dayofweek_origin_cat = pd.DataFrame(order_origin.groupby(['order_purchase_dayofweek', 'customer_state', 'product_category_name'], as_index=False)['order_id'].count())
order_dayofweek_top_origin_cat = order_dayofweek_origin_cat.loc[(order_dayofweek_origin_cat['customer_state'].isin(top_state_list) & order_dayofweek_origin_cat['product_category_name'].isin(top_cat_list))].reset_index().drop('index', axis=1)
order_dayofweek_top_origin_cat.sort_values('order_id', ascending=False)
order_dayofweek_top_origin_cat


# In[192]:


#showing lineplot of top states and top categrories based on day of week frequecncy
sns.set_style('darkgrid') # style 
sns.set(rc={'figure.figsize':(10,5)}) #mengatur ukuran gambar

ax = sns.lineplot(data=order_dayofweek_top_origin_cat, x ='order_purchase_dayofweek', y = 'order_id',
                  hue='customer_state', palette='Set2',
                  legend='full', lw=3) #membuat lineplot
sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
ax.xaxis.set_major_locator(ticker.MultipleLocator(1)) #mengatur sumbu x bertambah 1
plt.title('Day of Week/Origin Sales Frequency')
plt.ylabel('Sales')
plt.xlabel('Day of Week')
plt.show()

ax = sns.lineplot(data=order_dayofweek_top_origin_cat, x ='order_purchase_dayofweek', y = 'order_id',
                  hue='product_category_name', palette='Set2',
                  legend='full', lw=3) #membuat lineplot
sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
ax.xaxis.set_major_locator(ticker.MultipleLocator(1)) #mengatur sumbu x bertambah 1
plt.title('Day of Week/Product Sales Frequency')
plt.ylabel('Sales')
plt.xlabel('Day of Week')
plt.show()


# In[121]:


order_day_origin_cat = pd.DataFrame(order_origin.groupby(['order_purchase_day', 'customer_state', 'product_category_name'], as_index=False)['order_id'].count())
order_day_top_origin_cat = order_day_origin_cat.loc[(order_day_origin_cat['customer_state'].isin(top_state_list) & order_day_origin_cat['product_category_name'].isin(top_cat_list))].reset_index().drop('index', axis=1)
order_day_top_origin_cat.sort_values('order_id', ascending=False)
order_day_top_origin_cat


# In[193]:


#showing lineplot of top states and top categrories based on day frequecncy
sns.set_style('darkgrid') # style 
sns.set(rc={'figure.figsize':(10,5)}) #mengatur ukuran gambar

ax = sns.lineplot(data=order_day_top_origin_cat, x ='order_purchase_day', y = 'order_id',
                  hue='customer_state', palette='Set2',
                  legend='full', lw=3) #membuat lineplot
sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
ax.xaxis.set_major_locator(ticker.MultipleLocator(1)) #mengatur sumbu x bertambah 1
plt.title('Daily/Origin Sales Frequency')
plt.ylabel('Sales')
plt.xlabel('Day')
plt.show()

ax = sns.lineplot(data=order_day_top_origin_cat, x ='order_purchase_day', y = 'order_id',
                  hue='product_category_name', palette='Set2',
                  legend='full', lw=3) #membuat lineplot
sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
ax.xaxis.set_major_locator(ticker.MultipleLocator(1)) #mengatur sumbu x bertambah 1
plt.title('Daily/Product Sales Frequency')
plt.ylabel('Sales')
plt.xlabel('Day')
plt.show()


# In[123]:


order_origin.head()


# In[126]:


#create a pivot showing mean delivery time from each states to each states
delivery_time = order_origin.pivot_table(values='order_delivery_time', index='seller_state', columns='customer_state', aggfunc='mean', margins=True).sort_values('All', ascending=False)
delivery_time


# In[127]:


sns.heatmap(delivery_time)


# In[128]:


delivery_time.describe()['All']


# In[173]:


#showing pivot table of top customer states
delivery_time_top = order_origin[order_origin['customer_state'].isin(top_state_list)].pivot_table(values='order_delivery_time', index='seller_state', columns='customer_state', aggfunc='mean', margins=True).sort_values('All', ascending=False)
delivery_time_top


# In[174]:


sns.heatmap(delivery_time_top)


# In[129]:


#create a pivot showing mean estiamtion time gap from each states to each states
estimation_gap = order_origin.pivot_table(values='order_estimation_time_gap', index='seller_state', columns='customer_state', aggfunc='mean', margins=True).sort_values('All', ascending=False)
estimation_gap


# In[130]:


sns.heatmap(estimation_gap)


# In[131]:


estimation_gap.describe()['All']


# In[175]:


#showing pivot table of top customer states
estimation_gap_top = order_origin[order_origin['customer_state'].isin(top_state_list)].pivot_table(values='order_estimation_time_gap', index='seller_state', columns='customer_state', aggfunc='mean', margins=True).sort_values('All', ascending=False)
estimation_gap_top


# In[176]:


sns.heatmap(estimation_gap_top)


# In[134]:


'''
create a pivot showing handling time per state where handling time is defined as processing time
(how long seller takes order to the carrier service) and carrier time
(how long carrier service takes order to the customer)
and show its difference to mean for each phase
'''
handling_time = order_origin[['seller_state', 'order_process_time', 'order_carrier_time']].groupby('seller_state').mean().sort_values('order_process_time', ascending=False)
handling_time['total_handling'] = handling_time['order_process_time'] + handling_time['order_carrier_time']
handling_time['%_diff_process_mean'] = handling_time['order_process_time']/handling_time['order_process_time'].mean()*100-100
handling_time['%_diff_carrier_mean'] = handling_time['order_carrier_time']/handling_time['order_carrier_time'].mean()*100-100
handling_time['%_diff_handling_mean'] = handling_time['total_handling']/handling_time['total_handling'].mean()*100-100
handling_time = handling_time[['order_process_time', '%_diff_process_mean', 'order_carrier_time', '%_diff_carrier_mean', 'total_handling', '%_diff_handling_mean']]
handling_time.sort_values('%_diff_handling_mean', ascending=False)


# In[135]:


sns.heatmap(handling_time[['%_diff_process_mean', '%_diff_carrier_mean', '%_diff_handling_mean']])


# In[136]:


order_origin['order_process_time'].describe()


# In[137]:


order_origin['order_carrier_time'].describe()


# In[138]:


order_origin.head()


# In[158]:


'''
show how much each category costs in each state where price is comprised of
the product price itself plus freight. Then the table shows its difference to the mean for each component
'''

price_per_cat = pd.DataFrame(order_origin.groupby(['product_category_name', 'seller_state'], as_index=False)[['price', 'freight_value']].mean())
price_per_cat['%_diff_price_median'] = price_per_cat['price']/price_per_cat['price'].median()*100-100
price_per_cat['%_diff_freight_median'] = price_per_cat['freight_value']/price_per_cat['freight_value'].median()*100-100
price_per_cat = price_per_cat[['product_category_name', 'seller_state', 'price', '%_diff_price_median', 'freight_value', '%_diff_freight_median']]
price_per_cat


# In[165]:


price_diff = price_per_cat.pivot_table(values='%_diff_price_median', index='product_category_name', columns='seller_state', aggfunc='mean')
price_diff


# In[166]:


sns.heatmap(price_diff)


# In[167]:


price_per_cat_top = price_per_cat.loc[(price_per_cat['seller_state'].isin(top_state_list) & price_per_cat['product_category_name'].isin(top_cat_list))].reset_index()
price_per_cat_top


# In[168]:


#showing pivot table of top seller states
price_diff_top = price_per_cat_top.pivot_table(values='%_diff_price_median', index='product_category_name', columns='seller_state', aggfunc='mean')
price_diff_top


# In[169]:


sns.heatmap(price_diff_top)


# In[144]:


freight_diff = price_per_cat.pivot_table(values='%_diff_freight_median', index='product_category_name', columns='seller_state', aggfunc='mean')
freight_diff


# In[145]:


sns.heatmap(freight_diff)


# In[170]:


#showing pivot table of top seller states
freight_diff_top = price_per_cat_top.pivot_table(values='%_diff_freight_median', index='product_category_name', columns='seller_state', aggfunc='mean')
freight_diff_top


# In[171]:


sns.heatmap(freight_diff_top)


# In[95]:


'''
showing how customers from each state give reviews to sellers from each state
'''
review_time = order_origin.pivot_table(values='review_process_time', index='seller_state', columns='customer_state', aggfunc='mean', margins=True).sort_values('All', ascending=False)
review_time


# In[96]:


sns.heatmap(review_time)


# In[177]:


#showing pivot table of top seller and customer states
review_time_top = order_origin[(order_origin['seller_state'].isin(top_state_list)) & (order_origin['customer_state'].isin(top_state_list))].pivot_table(values='review_process_time', index='seller_state', columns='customer_state', aggfunc='mean', margins=True).sort_values('All', ascending=False)
review_time_top


# In[178]:


sns.heatmap(review_time_top)


# In[179]:


review_score = order_origin.pivot_table(values='order_id', index='seller_state', columns='review_score', aggfunc='count', margins=True).sort_values('All', ascending=False).drop(['All'])
review_score


# In[180]:


sns.heatmap(review_score)


# In[181]:


#showing pivot table of top seller states (who get the best reviews)
review_score_top = order_origin[(order_origin['seller_state'].isin(top_state_list)) & (order_origin['customer_state'].isin(top_state_list))].pivot_table(values='order_id', index='seller_state', columns='review_score', aggfunc='count', margins=True).sort_values('All', ascending=False).drop(['All'])
review_score_top


# In[182]:


sns.heatmap(review_score_top)

