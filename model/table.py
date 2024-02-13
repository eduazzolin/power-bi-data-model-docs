class Table:

    def __init__(self, id: str, name: str, columns: list, import_mode: str, power_query_steps: list, measures: list = None):
        self.id = id
        self.name = name
        self.columns = columns
        self.import_mode = import_mode
        self.power_query_steps = power_query_steps
        self.measures = measures
        self.queries = self.format_query()


    def __str__(self):
        power_query_steps = '\n    '.join(self.power_query_steps)
        columns = '\n   '.join(str(column) for column in self.columns)
        return f"""
{self.name}
{'-' * len(self.name)}
Import Mode: {self.import_mode}
Definition: 
    {power_query_steps}
Columns:
    {columns}
"""

    def format_query(self):
        queries = []
        for line in self.power_query_steps:
            if 'NativeQuery' in line:
                prefix: str = line[:line.find('[Data],') + 9]
                postfix: str = line[line.rfind(', null') - 1:]
                query: str = line[line.find('[Data],') + 9:line.rfind(', null') - 1]
                query = query.replace('#(lf)', '\n').replace('#(tab)', '    ')
                line = f'{prefix}\n{query}\n{postfix}'
                queries.append(query)
        return queries
        # "    Fonte = Value.NativeQuery(GoogleBigQuery.Database([BillingProject=\"dw-comodo\"]){[Name=\"dw-comodo\"]}[Data], \"SELECT#(lf)#(tab)'Facebook/Instagram' as canal,#(lf)#(tab)ad.account_id as customer_id,#(lf)#(tab)acc.name as costumer_name,#(lf)#(tab)ad.campaign_id,#(lf)#(tab)c.campaign_name,#(lf)#(tab)c.objective as campaign_type,#(lf)#(tab)c.status as campaign_status,#(lf)#(tab)c.created_time as campaign_created_time,#(lf)#(tab)c.updated_time as campaign_updated_time,#(lf)#(tab)c.daily_budget as campaign_daily_budget,#(lf)#(tab)ad.adset_id as adset_id,#(lf)#(tab)d.ad_sets_name as ad_set_name,#(lf)#(tab)d.status as ad_sets_status,#(lf)#(tab)d.created_time as  ad_sets_created_time,#(lf)#(tab)d.updated_time as  ad_sets_updated_time,#(lf)#(tab)CONCAT(left(d.targeting_age_min,2), ' - ', left(d.targeting_age_max,2)) as idade,#(lf)#(tab)case when d.targeting_genders = '[1]' then 'M'#(lf)#(tab)when d.targeting_genders = '[2]' then 'F'#(lf)#(tab)else '-' end as genero_publico,#(lf)#(tab)cast(d.daily_budget as int)/100 as ad_sets_daily_budget,#(lf)#(tab)d.targeting_geo_locations as localizacao,#(lf)#(tab)ad.ad_id ,#(lf)#(tab)ad.ad_name,#(lf)#(tab)ad.status as ad_status,#(lf)#(tab)ad.ad_manager_url as ad_destino,#(lf)#(tab)ad.created_time as ad_created_time,#(lf)#(tab)ad.updated_time as ad_updated_time#(lf)FROM#(lf)#(tab)dw_comodo.meta_dim_ads ad#(lf)join dw_comodo.meta_dim_accounts acc on #(lf)#(tab)ad.account_id = acc.account_id#(lf)left join dw_comodo.meta_dim_campanhas c on#(lf)#(tab)ad.campaign_id = c.campaign_id #(lf)left join dw_comodo.meta_dim_adsets d on#(lf)#(tab)ad.adset_id = d.ad_sets_id #(lf)where ad.ad_id is not null\", null, [EnableFolding=true]),",
