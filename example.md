# Sales & Returns Sample v201912
- Data do relatório: 15/02/2024 07:30:20

# Resumo do modelo de dados
- **Tamanho do modelo:** 11.86 MB
- **Quantidade de tabelas:** 16
- **Quantidade de relacionamentos:** 8
- **Quantidade de colunas:** 68
- **Quantidade de colunas calculadas:** 3
- **Quantidade de medidas:** 58

## Tabelas
1. [% Return Rate](#c0de6d6f-57dc-41b4-96e1-55ad0a9f5c58)
2. [Age](#d0dfd344-2155-483d-8fe2-2fd3caed3919)
3. [Analysis DAX](#445c1cb0-47b0-4e8b-986b-300a640b0447)
4. [Associated Product](#0d9001e2-0609-405a-9bce-9910b46307c9)
5. [Association](#6ca4907e-c8c9-4e62-ba5d-df131c88764f)
6. [Calendar](#715a3f9c-bea5-4323-948a-10b6ce711619)
7. [Customer](#a5974167-47c2-4f10-851b-a9b36245bddd)
8. [Design DAX](#27b86990-cbf9-49a1-9d2e-d8ee7816e592)
9. [Details](#c675f364-7e23-4cf7-94fa-fabea9a19d7e)
10. [Issues and Promotions](#bfc7c642-2029-4822-8fa6-e2079db05177)
11. [Product](#3be38723-3807-48c3-8499-c993b496e66f)
12. [STable](#76bb6a8e-b0d3-45ce-8967-4eecad6c0e7c)
13. [Sales](#75eab034-20f7-4fa0-b260-ec8f45d41aa8)
14. [Store](#c7307aed-3a68-484f-b3db-37452c0fc65a)
15. [Tooltip Info](#7432e6f3-572b-45c5-8b2c-1b5a40875212)
16. [Tooltip Info2](#8bac4bd0-5a88-4109-9d30-dea2a64c36b8)

## Relacionamentos

|  |  |  |  |  |
| ---- | ---- | ---- | ---- | ---- |
| Associated Product[ProductID] | one |  --->  | many | Association[RightItemSetId]
| (Desativado) *Associated Product[Product]* | *one* |  <-->  | *one* | *Product[Product]*
| Associated Product[Product] | one |  --->  | many | Customer[Product]
| Calendar[Date] | one |  --->  | many | Sales[Date]
| Product[ProductID] | one |  --->  | many | Sales[ProductID]
| Product[ProductID] | one |  --->  | many | Association[LeftItemSetId]
| Sales[ID] | one |  <-->  | one | Customer[ID]
| Store[StoreID] | one |  --->  | many | Sales[StoreID]
|  |  |  |  |  |

## Medidas
1. [% Return Rate Value](#db190b46-face-4bb4-ad12-fef64850d74b)
2. [Last 2 Months Net Sales](#476b56d5-ccb7-4f18-a60a-d1ed841caaf7)
3. [Last 2 Months Returns](#81e36c3f-3f30-4970-ac53-6009af8b216b)
4. [Net Sales](#cd2e7756-eb39-41a6-a73c-36aecb7b43c8)
5. [Net Sales PM](#b71875ff-9152-49a3-9651-654f7beb05e9)
6. [Net Sales Variance](#ea94c27a-07f9-4dcb-9c51-33ecf46a07b2)
7. [Net Sales Variance %](#2263b9a4-5117-4e64-a425-7236388fc050)
8. [Profit Difference](#aa35df95-aff7-4d3d-a722-1955ce6aee72)
9. [Return Rate](#c3645989-c086-47ba-af31-e12ac4d4d52c)
10. [Returns](#09023869-ae68-4a3a-9d35-a6becc131965)
11. [Returns PM](#eccc0c03-68f2-488a-9858-acaa5ec1d949)
12. [Returns Variance](#5751baf5-17f8-4fae-849d-1f17457f0d15)
13. [Returns Variance %](#936690a6-4116-4d5b-93b7-6c64656a625a)
14. [Total Return Rate](#ee417d6a-8fd1-4caf-a61b-fc8b79f72aa0)
15. [Units Returned](#56a36fdf-16d1-46a9-b22d-63f6f074374d)
16. [Units Returned PM](#6b4eb375-20c9-4c6b-ab5a-d750c863bfb8)
17. [Units Returned Variance %](#c0856a37-73e9-41a6-99f1-297c427cb949)
18. [Units Sold](#4f6b44ec-7552-484e-bd67-124e67a7c385)
19. [Units Sold PM](#d51c6348-be52-401c-a2c7-677e67d72580)
20. [Units Sold Variance %](#7ce11e74-aa12-487e-a6af-cbbd11542942)
21. [WIF Adjusted Net Sales](#89f3d61f-24b1-4b8a-a8b8-846c36501d89)
22. [WIF Adjusted Sales](#a0a4e80c-7645-44df-88d3-be04f39594dd)
23. [WIF Adjusted Units Returned](#4da2584d-d264-4f58-afb1-d6c7d29b9324)
24. [WIF Forecast](#a19bf6bc-3767-4b5f-b56d-9a6658a817af)
25. [WIF Price per Unit](#74cedb53-7f30-40dc-929a-93609a0a53f8)
26. [WIF Profit](#b524dc1e-e1ba-4267-91d2-c57ef6ffa1b8)
27. [WIF Profit Difference](#99a97246-6fb3-4d03-b0d9-7814afa5562d)
28. [WIF Sales](#9aea99a5-0f7a-421f-847b-e81ae3188e19)
29. [WIF Same](#5fe6697f-11ee-4ae5-92b2-6bed10f4326e)
30. [WIF Total Forecast](#6706b1b0-20a7-43a0-b08c-f6df7eba75ea)
31. [WIF Total Profit](#1bed2507-7783-49f6-9a2a-61eb07a646ab)
32. [WIF Units Returned](#66092a0d-befe-4048-8c0f-9828990a5333)
33. [WIF Units Returned Average](#9d462e15-7dd7-4344-bca7-a938a314eb8b)
34. [WIF Units Returned Difference](#95f5e193-f587-47d6-aa98-be16ec2cf701)
35. [WIF Units Returned_1](#978a4e31-2673-45a2-be8b-86bdd31dfd8d)
36. [WIF Units Returned_2](#b365a446-2b19-472e-bab1-6dd79ad89b11)
37. [Association](#0bbec620-3993-42f9-8ab8-4788bbd28c8d)
38. [Lift Label](#bd8f047a-5191-4ae1-8285-2171f92cc87e)
39. [Net Sales Indicator](#accde1a4-a2a2-443a-86ca-6eaab82bfdfa)
40. [Net Sales Label](#2c2aba58-11b5-46fe-b7eb-cbe0c0104c4e)
41. [Product Returns Other](#367f6c9d-55d0-47b9-8e30-c89c0cc7395c)
42. [Product Returns Top 3](#b4563709-dec3-4d36-ae79-b62dfb1b7cdc)
43. [Product Sales Other](#a7e1c109-6b22-4917-a399-0ef8894e5905)
44. [Product Sales Top 3](#77e6397d-9393-4f69-bda9-967d1450c25f)
45. [Product Top N](#bd89d675-790d-483d-9345-482d5ebe0793)
46. [ProductR Top N](#8d4c4464-d0f4-4d19-a792-f2f87a611f1c)
47. [Profit Indicator](#348fd79f-f753-46c2-916a-b4cebce661e9)
48. [Returns Indicator](#aa96d238-fd5d-47d1-912c-7ec33c7eaf7f)
49. [Returns Sales Top 3](#0f1aad1b-3133-47ba-ad15-0647e4ff2edc)
50. [Store Returns Other](#19dbac15-d8d6-4f41-9c64-edae27b890ed)
51. [Store Sales Other](#3eab07c9-cb2c-499c-98cb-dfb2d5ff6020)
52. [Store Sales Top 3](#bf92dbc2-b1be-43f3-98dd-c4b3ed64bbc9)
53. [Store Top N](#f92389cb-2c3a-4d75-8bd2-8e9dd803ed67)
54. [StoreR Top N](#271ce902-3d46-40e1-bda4-a5de9668ee00)
55. [Units Returned Indicator](#a92707dc-7269-4c1a-84c8-594209bc9176)
56. [Units Sold Indicator](#1288eecb-9cb6-40f6-8a7a-6059323bb594)
57. [Info Tooltip](#3a13ef24-a51d-44ee-b493-0f98326de4a7)
58. [Info Tooltip 2](#cd21eec8-425f-4973-9f6a-118edfe2e7ec)

# Detalhamento das tabelas

<a id="c0de6d6f-57dc-41b4-96e1-55ad0a9f5c58"></a>

## % Return Rate
- **Nome:** % Return Rate
- **Tipo:** calculated
- **Modo de importação:** import

### Medidas
1. [% Return Rate Value](#db190b46-face-4bb4-ad12-fef64850d74b)

### Definição no PowerQuery:
```M
GENERATESERIES(0, 60, 1)
```

<a id="d0dfd344-2155-483d-8fe2-2fd3caed3919"></a>

## Age
- **Nome:** Age
- **Tipo:** table
- **Modo de importação:** import

### Colunas
1. Age
2. Age Bucket

### Definição no PowerQuery:
```M
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("dc8rDsAgEIThqxA0AnZZHmchCER1k7amty+gaMKYEZ/6pxTtRJs+6jkVWfUe7bp1Nd0D8Ag8Ac97JwvcdSc3XVYn4AzcAxfg4y+F4fzricAT8Lx3tsDHX549vPYwAWfgHrhsvH4=", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [Age = _t, #"Age Bucket" = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Age", Int64.Type}, {"Age Bucket", type text}})
in
    #"Changed Type"
```

<a id="445c1cb0-47b0-4e8b-986b-300a640b0447"></a>

## Analysis DAX
- **Nome:** Analysis DAX
- **Tipo:** table
- **Modo de importação:** import

### Medidas
1. [Last 2 Months Net Sales](#476b56d5-ccb7-4f18-a60a-d1ed841caaf7)
2. [Last 2 Months Returns](#81e36c3f-3f30-4970-ac53-6009af8b216b)
3. [Net Sales](#cd2e7756-eb39-41a6-a73c-36aecb7b43c8)
4. [Net Sales PM](#b71875ff-9152-49a3-9651-654f7beb05e9)
5. [Net Sales Variance](#ea94c27a-07f9-4dcb-9c51-33ecf46a07b2)
6. [Net Sales Variance %](#2263b9a4-5117-4e64-a425-7236388fc050)
7. [Profit Difference](#aa35df95-aff7-4d3d-a722-1955ce6aee72)
8. [Return Rate](#c3645989-c086-47ba-af31-e12ac4d4d52c)
9. [Returns](#09023869-ae68-4a3a-9d35-a6becc131965)
10. [Returns PM](#eccc0c03-68f2-488a-9858-acaa5ec1d949)
11. [Returns Variance](#5751baf5-17f8-4fae-849d-1f17457f0d15)
12. [Returns Variance %](#936690a6-4116-4d5b-93b7-6c64656a625a)
13. [Total Return Rate](#ee417d6a-8fd1-4caf-a61b-fc8b79f72aa0)
14. [Units Returned](#56a36fdf-16d1-46a9-b22d-63f6f074374d)
15. [Units Returned PM](#6b4eb375-20c9-4c6b-ab5a-d750c863bfb8)
16. [Units Returned Variance %](#c0856a37-73e9-41a6-99f1-297c427cb949)
17. [Units Sold](#4f6b44ec-7552-484e-bd67-124e67a7c385)
18. [Units Sold PM](#d51c6348-be52-401c-a2c7-677e67d72580)
19. [Units Sold Variance %](#7ce11e74-aa12-487e-a6af-cbbd11542942)
20. [WIF Adjusted Net Sales](#89f3d61f-24b1-4b8a-a8b8-846c36501d89)
21. [WIF Adjusted Sales](#a0a4e80c-7645-44df-88d3-be04f39594dd)
22. [WIF Adjusted Units Returned](#4da2584d-d264-4f58-afb1-d6c7d29b9324)
23. [WIF Forecast](#a19bf6bc-3767-4b5f-b56d-9a6658a817af)
24. [WIF Price per Unit](#74cedb53-7f30-40dc-929a-93609a0a53f8)
25. [WIF Profit](#b524dc1e-e1ba-4267-91d2-c57ef6ffa1b8)
26. [WIF Profit Difference](#99a97246-6fb3-4d03-b0d9-7814afa5562d)
27. [WIF Sales](#9aea99a5-0f7a-421f-847b-e81ae3188e19)
28. [WIF Same](#5fe6697f-11ee-4ae5-92b2-6bed10f4326e)
29. [WIF Total Forecast](#6706b1b0-20a7-43a0-b08c-f6df7eba75ea)
30. [WIF Total Profit](#1bed2507-7783-49f6-9a2a-61eb07a646ab)
31. [WIF Units Returned](#66092a0d-befe-4048-8c0f-9828990a5333)
32. [WIF Units Returned Average](#9d462e15-7dd7-4344-bca7-a938a314eb8b)
33. [WIF Units Returned Difference](#95f5e193-f587-47d6-aa98-be16ec2cf701)
34. [WIF Units Returned_1](#978a4e31-2673-45a2-be8b-86bdd31dfd8d)
35. [WIF Units Returned_2](#b365a446-2b19-472e-bab1-6dd79ad89b11)

### Definição no PowerQuery:
```M
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Column1", type text}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"Column1"})
in
    #"Removed Columns"
```

<a id="0d9001e2-0609-405a-9bce-9910b46307c9"></a>

## Associated Product
- **Nome:** Associated Product
- **Tipo:** table
- **Modo de importação:** import

### Colunas
1. Product
2. Product Image
3. ProductID

### Relacionamentos
|  |  |  |  |  |
| ---- | ---- | ---- | ---- | ---- |
| Associated Product[ProductID] | one |   -->   | many | Association[RightItemSetId] |
| Associated Product[Product] | one |   -->   | many | Customer[Product] |
| (Desativado) *Associated Product[Product]* | *one* |   <->   | *one* | *Product[Product]*
|  |  |  |  |  |

### Definição no PowerQuery:
```M
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("ldRZb4JAEAfw78KzcZi9t2/W2Naj1mIPj/igqIgUKohH/fTdpgn7urwQQvILs7P/mfncQ6/h7crycLwDiNNlFN82RfPvZXPcLcOkGX6n5nukCQNUSoB4jMOo1zxkkbdozD3iyhFQM2iX/tvqqdLUVVNQVEvo58ktsJy51y4oJ9CN8mTUrzh3/zvVgkEsHtYdrLhwP7pA8wjWpwvfV1y6Fy+F1JAEcRG0K65qNN7nAkL6Lrv23rT72SWa1p1n3UnxVXH069w7UdDJsvQSW18jdspHCS013OYd651zR4Ci0kB7sdrb5qNz8gggckh/Xgq/a3mN5CkU8OEPR9uV5c7JQ2AoKezOvfZAW+8cPQKEMwW3oxy2fOtrZA8JkTC+5odka71z+CgwxXzI0uHs+WS9c/rM6FAzeVxdp/xml45z+ogZPVSw+jy2cmm9c/oIKKIF3HOcFtx65/SZ/jGN8DoWk/hgfY29h8rUv+7sB1lqfZ3Fx83anZTlfhD9+8Uv", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [ProductID = _t, #"Product Image" = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"ProductID", Int64.Type}, {"Product Image", type text}}),
    #"Merged Queries" = Table.NestedJoin(#"Changed Type", {"ProductID"}, Product, {"ProductID"}, "Product", JoinKind.LeftOuter),
    #"Expanded Product" = Table.ExpandTableColumn(#"Merged Queries", "Product", {"Product"}, {"Product.1"}),
    #"Renamed Columns" = Table.RenameColumns(#"Expanded Product",{{"Product.1", "Product"}})
in
    #"Renamed Columns"
```

### Colunas calculadas

**Segmented by**
```dax
"#ffffff"
```

<a id="6ca4907e-c8c9-4e62-ba5d-df131c88764f"></a>

## Association
- **Nome:** Association
- **Tipo:** table
- **Modo de importação:** import

### Colunas
1. Importance
2. LeftItemSetId
3. Probability
4. RightItemSetId
5. RuleID
6. Support

### Relacionamentos
|  |  |  |  |  |
| ---- | ---- | ---- | ---- | ---- |
| Association[RightItemSetId] | one |   <--   | many | Associated Product[ProductID] |
| Association[LeftItemSetId] | one |   <--   | many | Product[ProductID] |
|  |  |  |  |  |

### Definição no PowerQuery:
```M
let
    Source = Excel.Workbook(File.Contents("C:\Users\mimyersm\Dropbox\Data-27-09-2019.xlsx"), null, true),
    Association_Sheet = Source{[Item="Association",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Association_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"RuleID", Int64.Type}, {"LeftItemSetId", Int64.Type}, {"RightItemSetId", Int64.Type}, {"Probability", type number}, {"Importance", type number}, {"Support", Int64.Type}}),
    #"Inserted Merged Column" = Table.AddColumn(#"Changed Type", "Merged", each Text.Combine({Text.From([LeftItemSetId], "en-CA"), Text.From([RightItemSetId], "en-CA")}, ""), type text),
    #"Removed Duplicates" = Table.Distinct(#"Inserted Merged Column", {"Merged"}),
    #"Removed Columns" = Table.RemoveColumns(#"Removed Duplicates",{"Merged"})
in
    #"Removed Columns"
```

<a id="715a3f9c-bea5-4323-948a-10b6ce711619"></a>

## Calendar
- **Nome:** Calendar
- **Tipo:** table
- **Modo de importação:** import

### Colunas
1. Date
2. Month
3. MonthSort
4. Week

### Relacionamentos
|  |  |  |  |  |
| ---- | ---- | ---- | ---- | ---- |
| Calendar[Date] | one |   -->   | many | Sales[Date] |
|  |  |  |  |  |

### Definição no PowerQuery:
```M
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("fZSxisMwDIZfJWQuqSQ7dtztlg6FPkHpkIMbrxyFG+7tq4vcwD9I4IQUvg/kfk5ut5H4qEuI28ByItI1rNPwPY2HkfW6rI/+xOP9oHzxeQFeNp6Tzyfg08YL+XwGPhtffX4Gfrb5dR5x+KLX+euz76TY/OTzFfhqfPX5BfjF5s8+34Bv+/zJ60V6u67P/tfqz/cOXIPR4H0PriFoyL4L10hoWOfEgZHRsNKkU2XP+E/98fPsh4StNefAKGhYbeHAqGhYb1kCY0HDitN81OUYbdv5Xz+8bM1ZfEMIDOnNW2AwGtZcSmAIGtZcj61+DBxje7V/H/2lEmtOLTAyGtacS2DMaFhzSYFR0LDmiQKjoqHN7y8=", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [Date = _t, Week = _t, #"Month Name" = _t, MonthSort = _t, #"Week of Year" = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Date", type datetime}, {"Week", Int64.Type}, {"Month Name", type text}, {"MonthSort", Int64.Type}, {"Week of Year", Int64.Type}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"Month Name", "Month"}}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Renamed Columns",{{"Date", type date}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type1",{"Week of Year"})
in
    #"Removed Columns"
```

### Colunas calculadas

**Empty**
```dax
""
```

<a id="a5974167-47c2-4f10-851b-a9b36245bddd"></a>

## Customer
- **Nome:** Customer
- **Tipo:** table
- **Modo de importação:** import

### Colunas
1. Age
2. Amount
3. Category
4. Gender
5. ID
6. Issue
7. Price Range
8. Product
9. Promotion
10. Segment
11. Store
12. Type
13. Unit

### Relacionamentos
|  |  |  |  |  |
| ---- | ---- | ---- | ---- | ---- |
| Customer[ID] | one |   <->   | one | Sales[ID] |
| Customer[Product] | one |   <--   | many | Associated Product[Product] |
|  |  |  |  |  |

### Definição no PowerQuery:
```M
let
    Source = Excel.Workbook(File.Contents("C:\Users\mimyersm\Desktop\Sales & Marketing Datas.xlsx"), null, true),
    Data_Sheet = Source{[Item="Data",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Data_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"ID", Int64.Type}, {"ProductID", Int64.Type}, {"StoreID", Int64.Type}, {"Unit", Int64.Type}, {"Week", Int64.Type}, {"Gender", type text}, {"Age", Int64.Type}, {"Status", type text}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"Status"}),
    #"Merged Queries" = Table.NestedJoin(#"Removed Columns", {"ProductID"}, Product, {"ProductID"}, "Product", JoinKind.LeftOuter),
    #"Expanded Product" = Table.ExpandTableColumn(#"Merged Queries", "Product", {"Product", "Category", "Segment", "Price", "Price Range"}, {"Product.1", "Category", "Segment", "Price", "Price Range"}),
    #"Renamed Columns" = Table.RenameColumns(#"Expanded Product",{{"Product.1", "Product"}}),
    #"Removed Columns1" = Table.RemoveColumns(#"Renamed Columns",{"ProductID"}),
    #"Replaced Value" = Table.ReplaceValue(#"Removed Columns1","M","Male",Replacer.ReplaceText,{"Gender"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value","F","Female",Replacer.ReplaceText,{"Gender"}),
    #"Merged Queries1" = Table.NestedJoin(#"Replaced Value1", {"StoreID"}, Store, {"StoreID"}, "Store", JoinKind.LeftOuter),
    #"Expanded Store" = Table.ExpandTableColumn(#"Merged Queries1", "Store", {"Store", "Type"}, {"Store.1", "Type"}),
    #"Renamed Columns1" = Table.RenameColumns(#"Expanded Store",{{"Store.1", "Store"}}),
    #"Merged Queries2" = Table.NestedJoin(#"Renamed Columns1", {"ID"}, #"Issues and Promotions", {"ID"}, "Issues and Promotions", JoinKind.LeftOuter),
    #"Removed Columns2" = Table.RemoveColumns(#"Merged Queries2",{"StoreID"}),
    #"Expanded Issues and Promotions" = Table.ExpandTableColumn(#"Removed Columns2", "Issues and Promotions", {"Issue", "Promotion"}, {"Issue", "Promotion"}),
    #"Removed Columns3" = Table.RemoveColumns(#"Expanded Issues and Promotions",{"Week"}),
    #"Merged Queries3" = Table.NestedJoin(#"Removed Columns3", {"ID"}, Sales, {"ID"}, "Sales", JoinKind.LeftOuter),
    #"Expanded Sales" = Table.ExpandTableColumn(#"Merged Queries3", "Sales", {"Amount"}, {"Amount"}),
    #"Merged Queries4" = Table.NestedJoin(#"Expanded Sales", {"Age"}, Age, {"Age"}, "Age.1", JoinKind.LeftOuter),
    #"Expanded Age.1" = Table.ExpandTableColumn(#"Merged Queries4", "Age.1", {"Age Bucket"}, {"Age Bucket"}),
    #"Removed Columns4" = Table.RemoveColumns(#"Expanded Age.1",{"Age"}),
    #"Renamed Columns2" = Table.RenameColumns(#"Removed Columns4",{{"Age Bucket", "Age"}}),
    #"Removed Columns5" = Table.RemoveColumns(#"Renamed Columns2",{"Price"})
in
    #"Removed Columns5"
```

<a id="27b86990-cbf9-49a1-9d2e-d8ee7816e592"></a>

## Design DAX
- **Nome:** Design DAX
- **Tipo:** table
- **Modo de importação:** import

### Medidas
1. [Association](#0bbec620-3993-42f9-8ab8-4788bbd28c8d)
2. [Lift Label](#bd8f047a-5191-4ae1-8285-2171f92cc87e)
3. [Net Sales Indicator](#accde1a4-a2a2-443a-86ca-6eaab82bfdfa)
4. [Net Sales Label](#2c2aba58-11b5-46fe-b7eb-cbe0c0104c4e)
5. [Product Returns Other](#367f6c9d-55d0-47b9-8e30-c89c0cc7395c)
6. [Product Returns Top 3](#b4563709-dec3-4d36-ae79-b62dfb1b7cdc)
7. [Product Sales Other](#a7e1c109-6b22-4917-a399-0ef8894e5905)
8. [Product Sales Top 3](#77e6397d-9393-4f69-bda9-967d1450c25f)
9. [Product Top N](#bd89d675-790d-483d-9345-482d5ebe0793)
10. [ProductR Top N](#8d4c4464-d0f4-4d19-a792-f2f87a611f1c)
11. [Profit Indicator](#348fd79f-f753-46c2-916a-b4cebce661e9)
12. [Returns Indicator](#aa96d238-fd5d-47d1-912c-7ec33c7eaf7f)
13. [Returns Sales Top 3](#0f1aad1b-3133-47ba-ad15-0647e4ff2edc)
14. [Store Returns Other](#19dbac15-d8d6-4f41-9c64-edae27b890ed)
15. [Store Sales Other](#3eab07c9-cb2c-499c-98cb-dfb2d5ff6020)
16. [Store Sales Top 3](#bf92dbc2-b1be-43f3-98dd-c4b3ed64bbc9)
17. [Store Top N](#f92389cb-2c3a-4d75-8bd2-8e9dd803ed67)
18. [StoreR Top N](#271ce902-3d46-40e1-bda4-a5de9668ee00)
19. [Units Returned Indicator](#a92707dc-7269-4c1a-84c8-594209bc9176)
20. [Units Sold Indicator](#1288eecb-9cb6-40f6-8a7a-6059323bb594)

### Definição no PowerQuery:
```M
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Column1", type text}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"Column1"})
in
    #"Removed Columns"
```

<a id="c675f364-7e23-4cf7-94fa-fabea9a19d7e"></a>

## Details
- **Nome:** Details
- **Tipo:** table
- **Modo de importação:** import

### Colunas
1. DFSort
2. Design Factor
3. TSort
4. Topic

### Medidas
1. [Info Tooltip](#3a13ef24-a51d-44ee-b493-0f98326de4a7)
2. [Info Tooltip 2](#cd21eec8-425f-4973-9f6a-118edfe2e7ec)

### Definição no PowerQuery:
```M
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("lVXbcpswEP0VDc/OxMF2mjzKgBtNsWEwzmXSPChY2JrIKCNEU/ep39JP65dUK18mDYEQZjxjpLO7hz1npft7By98Esy8wOk5Z+YXxUGCUxLNcGjeXOehV4Ngs3eXEs8iBhYRhzidRMnUhvScOLoJEjQmyA/m39IoNkvD93Bo/yTsWSqNrjl7QWZ51JpzGo1JCFwuOqScykcu2DHzpQ1ZkNPFreXec0J8Fy1S+LJ+be+Qy5NFyUvNCo1CupWVBvhZDe5FYZTAltuYacozJUuZa5NTSFUCetCIvuKrNRTXipa25rAGHSd45pPZV9gddSgb5TnPOBUoVnJZZdoyOP9MYChX0kZ9qUWRWRokE7wzykVjUlLoimv+gwGsrsix64JRhXyqKfJN9xV/rDSXBehclyq4Nb49mNSta3NsqXw5SSVgmkXyqBBIS4SzQ71miaa84JtqY8jy7Ana4tY1MszAoHhPrlkmz/S6PIkF1blUG8A2K5MwIx9bGkMaX2ZbAO8EsdM5J3M7cz1nEuB0kQRz9L3q991z5OEYm/khKQkA4l68F3Qo4ituWjGVS5DKvfwQqtdKVqs1UO23gVMphebPgDtrw+2fv7//IJ/ltBIwBQO3Y8j+CIjpCugPBm1h17ysjLmvGF0yBehhxyL7T0Ep+2nJjT4Z94bkeVv4zZpqRHLAvav1AYcLKra/bL5WeV/RIUWmGC3Zqc92fyC4VfBXwRNeLA05phjSa17+N67Ivue52SygQcNWY0y40EyZbhRAYNhqjrGUTxuqnmC5qyUMs2dBt2jOBMu0GZ+d7hDQag9zCC85fI7xyMTMJtWaFysAdfWJPcfsoQ+Yzi7hWthOtPribZkxtTfL8GOTaJ5ZZFebwE2oKdyDfKdQZ4tIxbLdLTYyDnj4Bw==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [#"Design Factor" = _t, DFSort = _t, Topic = _t, TSort = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"DFSort", Int64.Type}, {"TSort", Int64.Type}})
in
    #"Changed Type"
```

<a id="bfc7c642-2029-4822-8fa6-e2079db05177"></a>

## Issues and Promotions
- **Nome:** Issues and Promotions
- **Tipo:** table
- **Modo de importação:** import

### Colunas
1. ID
2. Issue
3. Promotion

### Definição no PowerQuery:
```M
let
    Source = Excel.Workbook(File.Contents("C:\Users\mimyersm\Desktop\Sales & Marketing Datas.xlsx"), null, true),
    #"Issues and Promotions_Sheet" = Source{[Item="Issues and Promotions",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"Issues and Promotions_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"ID", Int64.Type}, {"Issue", type text}, {"Promotion", type text}})
in
    #"Changed Type"
```

<a id="3be38723-3807-48c3-8499-c993b496e66f"></a>

## Product
- **Nome:** Product
- **Tipo:** table
- **Modo de importação:** import

### Colunas
1. Category
2. Category Image
3. CategoryID
4. Price
5. Price Range
6. Product
7. Product Image
8. ProductID
9. Segement Color
10. Segment
11. Segment image
12. SegmentID

### Relacionamentos
|  |  |  |  |  |
| ---- | ---- | ---- | ---- | ---- |
| Product[ProductID] | one |   -->   | many | Sales[ProductID] |
| Product[ProductID] | one |   -->   | many | Association[LeftItemSetId] |
| (Desativado) *Product[Product]* | *one* |   <->   | *one* | *Associated Product[Product]*
|  |  |  |  |  |

### Definição no PowerQuery:
```M
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("xZlbU+JKEMe/imXt4+72ZC65nDcuwopCooAG9+xDhAEiIYFcUPj0ZwZxq04lW0UrWz4AIanBmV/9u/vf7c+f57XxWGbZ+ddzQ73c6TQcyzNmisONWzlR75Z6zfN8lf0DEC6DWbiT6Xd9IbN5MF58HydLdX/mUAoWowxYNiw6/vdVPDt2oQFUWAReLo3gKsYtdJgwwZ/vltdzzEIOnBEL/IF3wdhhoSDq7QsnZ9/Ovljk/NfXn+cXL2MZqbu0ik4nmEj1wY/HYwtHwLZ2PSEWZrMMTGFaENV/pCmSq6C2BfWXvvTu/g6eeRDPNAVWRaixDeLD5ZH7tZlgMBzE1m0NuV/DsYBGuS8SHFqHCg43IrBb0V8g5Mayl+RvMikB6qofjvNAXdnHq8jkFoPH0ct6scKJwbbVUZ+ajfVmizuqyYgNu2S6uUFFZxUjRx/034IQJn8zKvIoSRYa4ClExMHi1IaUR/MFSkRaC5Y6Z+HW2r1PA8Ttkoi85FmmXhLGuXpkVjFy00MYmsfLyDFsGN8+bYtnzJYpCFOR6sh2R2ZISIQbcPGUT9rso5BsUlKRVzxGYTaX6aFilRgNinRdJGH2lq2OPC5jnMHWn8otxXEyDdsBLtru3MGFqQpvBnGcLy47H+YkSpz68yCVb2KyTwaKgU2YBSzcxA83uPMawrCg77aKtvg0UGY5dfcX25VG4JwmKdnENGBN89YcuVnTsQU0zHbH739eUhIlPHdhFiYaAal0jsk2iM7qUSEP7ulYo2PZHLxCNC9RQaOslUFM6BGzNTaQ6Ywp2V4NZ+mPD9d/XhbRfZJqC21U2+t3QVKZm5ocwsFktOkiUxJ1YDhdT3yUizwpI6ucuf2662simsDhWqeddipljPPXDoXu3fXDCCUB1XyYjgkX7qB3E2AjzITheOI9LnE8qVrXMNPM7f1ZOco5NtNwo6VhVJprrG50ATZMWBRB3LlGNlmOcpzS9xcP409LQey3cRwrUHtEo2C53Nd7o9JcvyewtEvuxh5HBRYHw1H9Wf3+ub1rfR4gWgKko+nM7V1oIOLD0UWJJSATt5NZjuw7uLBgSu3WGIn1b8bX3lSf1S81G+2aX797UZBPk3R5oDSSUZQ8HzqTow0jERBNRlFjgDutan0NWDQv2WSDOy5XfQtMdhub2Mi/yGyYssud9/hnv3gVhLsg0i2qUWmr8T2+Y6jt+q77coXqshgY2lGncbJ20Xn6ZFFW0eMrzcTxax6q9NPYOZEe93ACV9vuHUF5RbWQKgkVsr99Qg2YTjonomYpD7VURO2HjJVe+l39hgGMKvcfDBcDnuLCxXIEgel4MWNPn9ZvUFKCtE9AtdUqe3tcykg6wXffMzGiWhtcsvkFcrq6b1qWs8hxZ0g92Q6DxOsOot0HUxIry2kgg72caKWr9op0Fb01bkfGDVXNOrhZcIezjoqsYakS1WNOiCptChCxTaiNBs0WsiZWaKnsjPp5qhjpZ5WTa+RcXzWvVBnAWer7HirWmFqoSv99XTYbyBIuVDGD0ZXkg9GH+fCygpJvTd280kpn/b6+TOUHrhJL4+l6fT3F7dlRUZbZtV0fNdA9aV/GWDlrv1qfPb7KXNSTSYzGxJWPJAS2de/+DlXG9XhWh2pv+Zgh/wtiOdyB2XAtQ2T/UspG1Pk/pl//AQ==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [Product = _t, ProductID = _t, Category = _t, CategoryID = _t, Segment = _t, SegmentID = _t, #"Product Image" = _t, #"Category Image" = _t, #"Segement Color" = _t, #"Segment image" = _t, Price = _t, #"Price Range" = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Product", type text}, {"ProductID", Int64.Type}, {"Category", type text}, {"CategoryID", Int64.Type}, {"Segment", type text}, {"SegmentID", Int64.Type}, {"Product Image", type text}, {"Category Image", type text}, {"Segement Color", type text}, {"Segment image", type text}, {"Price", Int64.Type}})
in
    #"Changed Type"
```

<a id="76bb6a8e-b0d3-45ce-8967-4eecad6c0e7c"></a>

## STable
- **Nome:** STable
- **Tipo:** table
- **Modo de importação:** import

### Colunas
1. Metric
2. Sort

### Definição no PowerQuery:
```M
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45Wci4tKkrNK1HwSy1RCE7MSS1W0lEyVIrViVZyrSgpSlQIKMpPyywBChopxcYCAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [Metric = _t, Sort = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Metric", type text}, {"Sort", Int64.Type}})
in
    #"Changed Type"
```

<a id="75eab034-20f7-4fa0-b260-ec8f45d41aa8"></a>

## Sales
- **Nome:** Sales
- **Tipo:** table
- **Modo de importação:** import

### Colunas
1. Amount
2. Date
3. ID
4. ProductID
5. Status
6. StoreID
7. Unit

### Relacionamentos
|  |  |  |  |  |
| ---- | ---- | ---- | ---- | ---- |
| Sales[ID] | one |   <->   | one | Customer[ID] |
| Sales[Date] | one |   <--   | many | Calendar[Date] |
| Sales[ProductID] | one |   <--   | many | Product[ProductID] |
| Sales[StoreID] | one |   <--   | many | Store[StoreID] |
|  |  |  |  |  |

### Definição no PowerQuery:
```M
let
    Source = Excel.Workbook(File.Contents("C:\Users\mimyersm\Desktop\Sales & Marketing Datas.xlsx"), null, true),
    Data_Sheet = Source{[Item="Data",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Data_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"ID", Int64.Type}, {"ProductID", Int64.Type}, {"StoreID", Int64.Type}, {"Unit", Int64.Type}, {"Week", Int64.Type}, {"Gender", type text}, {"Age", Int64.Type}, {"Status", type text}}),
    #"Replaced Value" = Table.ReplaceValue(#"Changed Type",1,2,Replacer.ReplaceValue,{"Week"}),
    #"Merged Queries" = Table.NestedJoin(#"Replaced Value", {"ProductID"}, Product, {"ProductID"}, "Product", JoinKind.LeftOuter),
    #"Expanded Product" = Table.ExpandTableColumn(#"Merged Queries", "Product", {"Price"}, {"Price"}),
    #"Inserted Multiplication" = Table.AddColumn(#"Expanded Product", "Multiplication", each [Price] * [Unit], Int64.Type),
    #"Renamed Columns" = Table.RenameColumns(#"Inserted Multiplication",{{"Multiplication", "Amount"}}),
    #"Removed Columns" = Table.RemoveColumns(#"Renamed Columns",{"Price"}),
    #"Merged Queries1" = Table.NestedJoin(#"Removed Columns", {"Week"}, Calendar, {"Week"}, "Calendar", JoinKind.LeftOuter),
    #"Expanded Calendar" = Table.ExpandTableColumn(#"Merged Queries1", "Calendar", {"Date"}, {"Date"}),
    #"Removed Columns1" = Table.RemoveColumns(#"Expanded Calendar",{"Week", "Gender", "Age"})
in
    #"Removed Columns1"
```

<a id="c7307aed-3a68-484f-b3db-37452c0fc65a"></a>

## Store
- **Nome:** Store
- **Tipo:** table
- **Modo de importação:** import

### Colunas
1. Latitude
2. Longitude
3. Store
4. StoreID
5. Type
6. image

### Relacionamentos
|  |  |  |  |  |
| ---- | ---- | ---- | ---- | ---- |
| Store[StoreID] | one |   -->   | many | Sales[StoreID] |
|  |  |  |  |  |

### Definição no PowerQuery:
```M
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("bZLNasNADITfxec0SPsjrY5paaFQSkohl5DDus3B4NjUsUsfv6tk7VKyJ8sLn0Yz0n5fYbWqNnUdz+n7+DMehy62qbwLvGZ21tv043At5MlKqqvDal8Zhdrma2oKFIrx2tWZNaBxxs2UtrqPQx1vIRJvxWQpH4TCDCn9HtvvqTSgMyySKUT6k/KpeIonVXru/jECQYAzA44uo14YSsXLsS/JMFp3RYJFNn5GtM8udpvh/HlsS6D3EK4gpwBhAfXxNY7TUMrCWnA5dnZgYHGlVrexLdmiQCZkW2yQabGFoFQzTKdbqQBANsfOQF4WKVR+259KlJcgIVMklI5kofT1bWrq0rYCIVieY0z7Ws4J1e1D3439uS9Ys4HAzJxmunA67q75GPuhKWXCHn3eG4ulfFSHXw==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [ManufacturerID = _t, Manufacturer = _t, Type = _t, Longitude = _t, Latitude = _t, image = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"ManufacturerID", Int64.Type}, {"Manufacturer", type text}, {"Type", type text}, {"Longitude", type number}, {"Latitude", type number}, {"image", type text}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"ManufacturerID", "StoreID"}, {"Manufacturer", "Store"}})
in
    #"Renamed Columns"
```

<a id="7432e6f3-572b-45c5-8b2c-1b5a40875212"></a>

## Tooltip Info
- **Nome:** Tooltip Info
- **Tipo:** table
- **Modo de importação:** import

### Colunas
1. DLINK
2. URL
3. nombre

### Definição no PowerQuery:
```M
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("pZJBT8IwGIb/SrMz8o2Wjs0bARLloEjkYAiHbpRtGWtnW8Dx651pQnBoCnprmqd93u/Nt1x6T9wgzbZcozuUMMNTqWoUK86KtTwIr+NlxlT6HiAvWZofuep+HbjOWFJ0E1k292mEMQQhjeCt3i/iXTfNN62H5zxUpeVSb9X5HkAbqfjt9j6QHgngMRTJ/Nlpl5a7tBe8RrnYbHdcJFzpa+09oNj3Ybpm40XltG8tZ+1zbnZK/K/6PlAa+MDHU1nE7uEt19a3ikfXywc4CEHF0xf24ZZbri3/Y+8YaN8PIA9mRZa5d85y526kmtIbvzjtwF6jQ8YMuvjr1xAECKGQPZTvi6Mzg7DcTxlu1GKIKA5hXkyS4at7dstZ70weuBpW1dU9E8DRIIJ1PZqQkXtGyzWu1Sc=", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [nombre = _t, URL = _t, DLINK = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"nombre", type text}, {"URL", type text}, {"DLINK", type text}})
in
    #"Changed Type"
```

### Colunas calculadas

**Empty**
```dax
" "
```

<a id="8bac4bd0-5a88-4109-9d30-dea2a64c36b8"></a>

## Tooltip Info2
- **Nome:** Tooltip Info2
- **Tipo:** table
- **Modo de importação:** import

### Colunas
1. DLINK
2. Nombre
3. URL

### Definição no PowerQuery:
```M
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45W8kstUQhOzEktVtBVCIwpNTAwMnNU0lHKKCkpKLbS18/MTUxPLc5ITM7WS87P1c/UL8gPKC8IzyhIR1OUWZVapIeuOjfd0shE39zU0kAfoksvPTNNKVYnWikotaS0KI9oS3PDvXLyAlOJttRI38LM1EgfogtiaSwA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [Nombre = _t, URL = _t, DLINK = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Nombre", type text}, {"URL", type text}, {"DLINK", type text}})
in
    #"Changed Type"
```

# Detalhamento das medidas

<a id="db190b46-face-4bb4-ad12-fef64850d74b"></a>

## % Return Rate Value
- **Nome:** % Return Rate Value
- **Tabela:** % Return Rate
- **Pasta:** Nenhuma
- **Formato:** ``Automático``

```dax
SELECTEDVALUE('% Return Rate'[% Return Rate])/100
```

<a id="476b56d5-ccb7-4f18-a60a-d1ed841caaf7"></a>

## Last 2 Months Net Sales
- **Nome:** Last 2 Months Net Sales
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``0``

```dax
[Net Sales]+[Net Sales PM]
```

<a id="81e36c3f-3f30-4970-ac53-6009af8b216b"></a>

## Last 2 Months Returns
- **Nome:** Last 2 Months Returns
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``0``

```dax
[Returns]+[Returns PM]
```

<a id="cd2e7756-eb39-41a6-a73c-36aecb7b43c8"></a>

## Net Sales
- **Nome:** Net Sales
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``\$#,0;-\$#,0;\$#,0``

```dax
CALCULATE(SUM(Sales[Amount]),Sales[Status]="Sold")
```

<a id="b71875ff-9152-49a3-9651-654f7beb05e9"></a>

## Net Sales PM
- **Nome:** Net Sales PM
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``\$#,0;-\$#,0;\$#,0``

```dax
CALCULATE([Net Sales],PREVIOUSMONTH('Calendar'[Date]))
```

<a id="ea94c27a-07f9-4dcb-9c51-33ecf46a07b2"></a>

## Net Sales Variance
- **Nome:** Net Sales Variance
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``\$#,0;-\$#,0;\$#,0``

```dax
[Net Sales]-[Net Sales PM]
```

<a id="2263b9a4-5117-4e64-a425-7236388fc050"></a>

## Net Sales Variance %
- **Nome:** Net Sales Variance %
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``0.0%;-0.0%;0.0%``

```dax
DIVIDE([Net Sales],[Net Sales PM],0)-1
```

<a id="aa35df95-aff7-4d3d-a722-1955ce6aee72"></a>

## Profit Difference
- **Nome:** Profit Difference
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``Automático``

```dax
DIVIDE([WIF Adjusted Sales],[Net Sales],0)-1
```

<a id="c3645989-c086-47ba-af31-e12ac4d4d52c"></a>

## Return Rate
- **Nome:** Return Rate
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``0%;-0%;0%``

```dax
DIVIDE((ROUND(((DIVIDE([Returns],SUM(Sales[Amount]),0))*100),0)),100,0)
```

<a id="09023869-ae68-4a3a-9d35-a6becc131965"></a>

## Returns
- **Nome:** Returns
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``\$#,0;-\$#,0;\$#,0``

```dax
CALCULATE(SUM(Sales[Amount]),Sales[Status]="Returned")
```

<a id="eccc0c03-68f2-488a-9858-acaa5ec1d949"></a>

## Returns PM
- **Nome:** Returns PM
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``0``

```dax
CALCULATE([Returns],PREVIOUSMONTH('Calendar'[Date]))
```

<a id="5751baf5-17f8-4fae-849d-1f17457f0d15"></a>

## Returns Variance
- **Nome:** Returns Variance
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``0``

```dax
[Returns]-[Returns PM]
```

<a id="936690a6-4116-4d5b-93b7-6c64656a625a"></a>

## Returns Variance %
- **Nome:** Returns Variance %
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``0.0%;-0.0%;0.0%``

```dax
(DIVIDE([Returns],[Returns PM],0)-1)
```

<a id="ee417d6a-8fd1-4caf-a61b-fc8b79f72aa0"></a>

## Total Return Rate
- **Nome:** Total Return Rate
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``0%;-0%;0%``

```dax
CALCULATE([Return Rate],ALL('Calendar'[Date].[Month]))
```

<a id="56a36fdf-16d1-46a9-b22d-63f6f074374d"></a>

## Units Returned
- **Nome:** Units Returned
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``#,0``

```dax
CALCULATE(SUM(Sales[Unit]),Sales[Status]="Returned")
```

<a id="6b4eb375-20c9-4c6b-ab5a-d750c863bfb8"></a>

## Units Returned PM
- **Nome:** Units Returned PM
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``0``

```dax
CALCULATE([Units Returned],PREVIOUSMONTH('Calendar'[Date]))
```

<a id="c0856a37-73e9-41a6-99f1-297c427cb949"></a>

## Units Returned Variance %
- **Nome:** Units Returned Variance %
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``Automático``

```dax
DIVIDE([Units Returned],[Units Returned PM],0)-1
```

<a id="4f6b44ec-7552-484e-bd67-124e67a7c385"></a>

## Units Sold
- **Nome:** Units Sold
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``#,0``

```dax
CALCULATE(SUM(Sales[Unit]),Sales[Status]="Sold")
```

<a id="d51c6348-be52-401c-a2c7-677e67d72580"></a>

## Units Sold PM
- **Nome:** Units Sold PM
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``#,0``

```dax
CALCULATE([Units Sold],PREVIOUSMONTH('Calendar'[Date]))
```

<a id="7ce11e74-aa12-487e-a6af-cbbd11542942"></a>

## Units Sold Variance %
- **Nome:** Units Sold Variance %
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``Automático``

```dax
DIVIDE([Units Sold],[Units Sold PM],0)-1
```

<a id="89f3d61f-24b1-4b8a-a8b8-846c36501d89"></a>

## WIF Adjusted Net Sales
- **Nome:** WIF Adjusted Net Sales
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``\$#,0;-\$#,0;\$#,0``

```dax
(SUM(Sales[Unit])*[WIF Price per Unit])-DIVIDE((SUM(Sales[Unit])*'% Return Rate'[% Return Rate Value]),1,0)*[WIF Price per Unit]
```

<a id="a0a4e80c-7645-44df-88d3-be04f39594dd"></a>

## WIF Adjusted Sales
- **Nome:** WIF Adjusted Sales
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``Automático``

```dax
[WIF Units Returned_1]*[WIF Price per Unit]
```

<a id="4da2584d-d264-4f58-afb1-d6c7d29b9324"></a>

## WIF Adjusted Units Returned
- **Nome:** WIF Adjusted Units Returned
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``Automático``

```dax
DIVIDE((SUM(Sales[Unit])*'% Return Rate'[% Return Rate Value]),1,0)
```

<a id="a19bf6bc-3767-4b5f-b56d-9a6658a817af"></a>

## WIF Forecast
- **Nome:** WIF Forecast
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``\$#,0;-\$#,0;\$#,0``

```dax
[Net Sales]+[WIF Profit]
```

<a id="74cedb53-7f30-40dc-929a-93609a0a53f8"></a>

## WIF Price per Unit
- **Nome:** WIF Price per Unit
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``Automático``

```dax
DIVIDE([Net Sales],[Units Sold],0)
```

<a id="b524dc1e-e1ba-4267-91d2-c57ef6ffa1b8"></a>

## WIF Profit
- **Nome:** WIF Profit
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``\$#,0;-\$#,0;\$#,0``

```dax
IF([WIF Same]=0,0,IF(ROUNDDOWN([WIF Adjusted Net Sales]-[Net Sales],0)<0,0,ROUNDDOWN([WIF Adjusted Net Sales]-[Net Sales],0)))
```

<a id="99a97246-6fb3-4d03-b0d9-7814afa5562d"></a>

## WIF Profit Difference
- **Nome:** WIF Profit Difference
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``0.0%;-0.0%;0.0%``

```dax
DIVIDE([WIF Forecast],[Net Sales],0)-1
```

<a id="9aea99a5-0f7a-421f-847b-e81ae3188e19"></a>

## WIF Sales
- **Nome:** WIF Sales
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``\$#,0;-\$#,0;\$#,0``

```dax
CALCULATE([Net Sales],ALL('Calendar'[Date].[Month]))
```

<a id="5fe6697f-11ee-4ae5-92b2-6bed10f4326e"></a>

## WIF Same
- **Nome:** WIF Same
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``0``

```dax
IF([% Return Rate Value]>=CALCULATE([Return Rate],ALL(Store[Type]),ALL(Store[Store])),0,1)
```

<a id="6706b1b0-20a7-43a0-b08c-f6df7eba75ea"></a>

## WIF Total Forecast
- **Nome:** WIF Total Forecast
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``\$#,0;-\$#,0;\$#,0``

```dax
CALCULATE([WIF Forecast],ALL('Calendar'[Date].[Month]))
```

<a id="1bed2507-7783-49f6-9a2a-61eb07a646ab"></a>

## WIF Total Profit
- **Nome:** WIF Total Profit
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``\$#,0;-\$#,0;\$#,0``

```dax
CALCULATE([WIF Profit],ALL('Calendar'[Date].[Month]))
```

<a id="66092a0d-befe-4048-8c0f-9828990a5333"></a>

## WIF Units Returned
- **Nome:** WIF Units Returned
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``Automático``

```dax
IF([Units Returned]-[WIF Units Returned Average]<0,0,[Units Returned]-[WIF Units Returned Average])
```

<a id="9d462e15-7dd7-4344-bca7-a938a314eb8b"></a>

## WIF Units Returned Average
- **Nome:** WIF Units Returned Average
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``Automático``

```dax
DIVIDE([WIF Units Returned Difference],CALCULATE(DISTINCTCOUNT('Calendar'[Date]), ALL('Calendar')),0)
```

<a id="95f5e193-f587-47d6-aa98-be16ec2cf701"></a>

## WIF Units Returned Difference
- **Nome:** WIF Units Returned Difference
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``Automático``

```dax
[WIF Units Returned_1]-[WIF Units Returned_2]
```

<a id="978a4e31-2673-45a2-be8b-86bdd31dfd8d"></a>

## WIF Units Returned_1
- **Nome:** WIF Units Returned_1
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``0``

```dax
CALCULATE([Units Returned], ALLSELECTED('Calendar'[Date]))
```

<a id="b365a446-2b19-472e-bab1-6dd79ad89b11"></a>

## WIF Units Returned_2
- **Nome:** WIF Units Returned_2
- **Tabela:** Analysis DAX
- **Pasta:** Nenhuma
- **Formato:** ``Automático``

```dax
CALCULATE([WIF Adjusted Units Returned], ALLSELECTED('Calendar'[Date]))
```

<a id="0bbec620-3993-42f9-8ab8-4788bbd28c8d"></a>

## Association
- **Nome:** Association
- **Tabela:** Design DAX
- **Pasta:** Nenhuma
- **Formato:** ``Automático``

```dax
VALUE(CONCATENATE([Product Top N],(SUM(Association[Importance]))))
```

<a id="bd8f047a-5191-4ae1-8285-2171f92cc87e"></a>

## Lift Label
- **Nome:** Lift Label
- **Tabela:** Design DAX
- **Pasta:** Nenhuma
- **Formato:** ``Automático``

```dax
CONCATENATE(FORMAT(SUM(Association[Importance]),"0.0"),"x")
```

<a id="accde1a4-a2a2-443a-86ca-6eaab82bfdfa"></a>

## Net Sales Indicator
- **Nome:** Net Sales Indicator
- **Tabela:** Design DAX
- **Pasta:** Nenhuma
- **Formato:** ``Automático``

```dax
CONCATENATE(IF([Net Sales Variance %]<=0,"","+"),FORMAT([Net Sales Variance %],"0.0%"))
```

<a id="2c2aba58-11b5-46fe-b7eb-cbe0c0104c4e"></a>

## Net Sales Label
- **Nome:** Net Sales Label
- **Tabela:** Design DAX
- **Pasta:** Nenhuma
- **Formato:** ``Automático``

```dax
CONCATENATE("",FORMAT([Net Sales],"$0,000"))
```

<a id="367f6c9d-55d0-47b9-8e30-c89c0cc7395c"></a>

## Product Returns Other
- **Nome:** Product Returns Other
- **Tabela:** Design DAX
- **Pasta:** Nenhuma
- **Formato:** ``\$#,0.###############;(\$#,0.###############);\$#,0.###############``

```dax
IF([ProductR Top N]>3,[Returns],0)
```

<a id="b4563709-dec3-4d36-ae79-b62dfb1b7cdc"></a>

## Product Returns Top 3
- **Nome:** Product Returns Top 3
- **Tabela:** Design DAX
- **Pasta:** Nenhuma
- **Formato:** ``\$#,0;-\$#,0;\$#,0``

```dax
IF([ProductR Top N]<4,[Returns],0)
```

<a id="a7e1c109-6b22-4917-a399-0ef8894e5905"></a>

## Product Sales Other
- **Nome:** Product Sales Other
- **Tabela:** Design DAX
- **Pasta:** Nenhuma
- **Formato:** ``\$#,0;-\$#,0;\$#,0``

```dax
IF([Product Top N]>3,[Net Sales],0)
```

<a id="77e6397d-9393-4f69-bda9-967d1450c25f"></a>

## Product Sales Top 3
- **Nome:** Product Sales Top 3
- **Tabela:** Design DAX
- **Pasta:** Nenhuma
- **Formato:** ``\$#,0;-\$#,0;\$#,0``

```dax
IF([Product Top N]<4,[Net Sales],0)
```

<a id="bd89d675-790d-483d-9345-482d5ebe0793"></a>

## Product Top N
- **Nome:** Product Top N
- **Tabela:** Design DAX
- **Pasta:** Nenhuma
- **Formato:** ``0``

```dax
SWITCH(
    TRUE(),
    ISINSCOPE('Product'[Product]),
    RANKX(ALL('Product'[Product]),[Net Sales],,DESC),
    ISINSCOPE('Product'[Segment]),
    RANKX(ALL('Product'[Segment]),[Net Sales],,DESC),
    RANKX(ALL('Product'[Category]),[Net Sales],,DESC)
)
```

<a id="8d4c4464-d0f4-4d19-a792-f2f87a611f1c"></a>

## ProductR Top N
- **Nome:** ProductR Top N
- **Tabela:** Design DAX
- **Pasta:** Nenhuma
- **Formato:** ``0``

```dax
SWITCH(
    TRUE(),
    ISINSCOPE('Product'[Product]),
    RANKX(ALL('Product'[Product]),[Returns],,DESC),
    ISINSCOPE('Product'[Segment]),
    RANKX(ALL('Product'[Segment]),[Returns],,DESC),
    RANKX(ALL('Product'[Category]),[Returns],,DESC)
)
```

<a id="348fd79f-f753-46c2-916a-b4cebce661e9"></a>

## Profit Indicator
- **Nome:** Profit Indicator
- **Tabela:** Design DAX
- **Pasta:** Nenhuma
- **Formato:** ``Automático``

```dax
CONCATENATE(IF([WIF Profit Difference]<=0,"","+"),FORMAT([WIF Profit Difference],"0.0%"))
```

<a id="aa96d238-fd5d-47d1-912c-7ec33c7eaf7f"></a>

## Returns Indicator
- **Nome:** Returns Indicator
- **Tabela:** Design DAX
- **Pasta:** Nenhuma
- **Formato:** ``Automático``

```dax
CONCATENATE(IF([Returns Variance %]<=0,"","+"),FORMAT([Returns Variance %],"0.0%"))
```

<a id="0f1aad1b-3133-47ba-ad15-0647e4ff2edc"></a>

## Returns Sales Top 3
- **Nome:** Returns Sales Top 3
- **Tabela:** Design DAX
- **Pasta:** Nenhuma
- **Formato:** ``\$#,0;-\$#,0;\$#,0``

```dax
IF([StoreR Top N]<4,[Returns],0)
```

<a id="19dbac15-d8d6-4f41-9c64-edae27b890ed"></a>

## Store Returns Other
- **Nome:** Store Returns Other
- **Tabela:** Design DAX
- **Pasta:** Nenhuma
- **Formato:** ``\$#,0;-\$#,0;\$#,0``

```dax
IF([StoreR Top N]>3,[Returns],0)
```

<a id="3eab07c9-cb2c-499c-98cb-dfb2d5ff6020"></a>

## Store Sales Other
- **Nome:** Store Sales Other
- **Tabela:** Design DAX
- **Pasta:** Nenhuma
- **Formato:** ``\$#,0;-\$#,0;\$#,0``

```dax
IF([Store Top N]>3,[Net Sales],0)
```

<a id="bf92dbc2-b1be-43f3-98dd-c4b3ed64bbc9"></a>

## Store Sales Top 3
- **Nome:** Store Sales Top 3
- **Tabela:** Design DAX
- **Pasta:** Nenhuma
- **Formato:** ``\$#,0;-\$#,0;\$#,0``

```dax
IF([Store Top N]<4,[Net Sales],0)
```

<a id="f92389cb-2c3a-4d75-8bd2-8e9dd803ed67"></a>

## Store Top N
- **Nome:** Store Top N
- **Tabela:** Design DAX
- **Pasta:** Nenhuma
- **Formato:** ``0``

```dax
RANKX(ALL('Store'[Store]),[Net Sales],,DESC)
```

<a id="271ce902-3d46-40e1-bda4-a5de9668ee00"></a>

## StoreR Top N
- **Nome:** StoreR Top N
- **Tabela:** Design DAX
- **Pasta:** Nenhuma
- **Formato:** ``0``

```dax
RANKX(ALL('Store'[Store]),[Returns],,DESC)
```

<a id="a92707dc-7269-4c1a-84c8-594209bc9176"></a>

## Units Returned Indicator
- **Nome:** Units Returned Indicator
- **Tabela:** Design DAX
- **Pasta:** Nenhuma
- **Formato:** ``Automático``

```dax
CONCATENATE(IF([Returns Variance %]<=0,"","+"),FORMAT([Returns Variance %],"0.0%"))
```

<a id="1288eecb-9cb6-40f6-8a7a-6059323bb594"></a>

## Units Sold Indicator
- **Nome:** Units Sold Indicator
- **Tabela:** Design DAX
- **Pasta:** Nenhuma
- **Formato:** ``Automático``

```dax
CONCATENATE(IF([Units Sold Variance %]<=0,"","+"),FORMAT([Units Sold Variance %],"0.0%"))
```

<a id="3a13ef24-a51d-44ee-b493-0f98326de4a7"></a>

## Info Tooltip
- **Nome:** Info Tooltip
- **Tabela:** Details
- **Pasta:** Nenhuma
- **Formato:** ``Automático``

```dax
"https://imagizer.imageshack.com/img923/4052/lLHy3U.gif"
```

<a id="cd21eec8-425f-4973-9f6a-118edfe2e7ec"></a>

## Info Tooltip 2
- **Nome:** Info Tooltip 2
- **Tabela:** Details
- **Pasta:** Nenhuma
- **Formato:** ``Automático``

```dax
"https://imagizer.imageshack.com/img921/2483/uMs9ZQ.gif"
```
