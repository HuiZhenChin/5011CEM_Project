import pandas as pd
import numpy as np
import warnings
from scipy.stats import chi2_contingency
from scipy.stats import norm
import seaborn as sns
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')

product = pd.read_csv("olist_products_dataset.csv")
product_category = pd.read_csv("product_category_name_translation.csv")
payment = pd.read_csv("olist_order_payments_dataset.csv")
order_item = pd.read_csv("olist_order_items_dataset.csv")

# clean
payment = payment[payment['payment_type'] != 'not_defined']

payment.reset_index(drop=True, inplace=True)

# remove those null values row
product.dropna(inplace=True)

merged_step1 = payment.merge(order_item, on='order_id', how='inner')

merged_step2 = merged_step1.merge(product, on='product_id', how='inner')

merged_step3 = merged_step2.merge(product_category, left_on='product_category_name', right_on='product_category_name_english',
                                  how='left')

# categorize into 6 groups
category_to_group = {
    'electronics_technology_group': [
        'informatica_acessorios', 'tablets_impressao_imagem', 'eletroportateis', 'eletronicos', 'audio', 'pcs',
        'portateis_casa_forno_e_cafe', 'cine_foto'
    ],
    'fashion_apparel_group': [
        'fashion_bolsas_e_acessorios', 'fashion_calcados', 'fashion_roupa_masculina', 'fashion_underwear_e_moda_praia',
        'fashion_esporte', 'fashion_roupa_feminina', 'fashion_roupa_infanto_juvenil','fashion_roupa_masculina', 'fashion_underwear_e_moda_praia', 
        'fashion_esporte'
    ],
    'home_garden_group': [
        'cama_mesa_banho', 'moveis_decoracao', 'utilidades_domesticas', 'ferramentas_jardim',
        'moveis_cozinha_area_de_servico_jantar_e_jardim', 'moveis_colchao_e_estofado',
        'construcao_ferramentas_construcao', 'moveis_sala', 'construcao_ferramentas_jardim', 'moveis_escritorio',
        'eletrodomesticos', 'casa_conforto', 'construcao_ferramentas_ferramentas', 'moveis_quarto',
        'construcao_ferramentas_iluminacao', 'casa_conforto_2', 'la_cuisine'
    ],
    'books_entertainment_group': [
        'livros_tecnicos', 'livros_interesse_geral', 'cds_dvds_musicais', 'dvds_blu_ray', 'musica', 'cds_dvds_musicals',
        'livros_importados', 'cds_dvds_musicais', 'dvds_blu_ray', 'musica', 'cds_dvds_musicals'
    ],
    'toys_hobbies_group': [
        'brinquedos', 'cool_stuff', 'malas_acessorios', 'construcao_ferramentas_construcao',
        'construcao_ferramentas_garden', 'pet_shop', 'fraldas_higiene', 'artigos_de_natal'
    ],
    'miscellaneous_group': [
        'automotivo', 'alimentos_bebidas', 'bebes', 'papelaria', 'alimentos', 'artes', 'sinalizacao_e_seguranca',
        'artigos_de_festas', 'construcao_ferramentas_seguranca', 'seguros_e_servicos', 'bebidas', 'flores',
        'fraldas_higiene', 'market_place', 'instrumentos_musicais', 'industria_comercio_e_negocios', 'aliments'
        
    ]
}

# create a new column 'product_category_group' based on the mapping
product['product_category_group'] = product['product_category_name'].apply(
    lambda category: next((group for group, categories in category_to_group.items() if category in categories),
                         'miscellaneous_group')
)

# merge
merged_step3['product_category_group'] = product['product_category_group']


# perform chi-squared tests for the relationship between payment types and product categories
observed = pd.crosstab(merged_step3['product_category_name_english'], merged_step3['payment_type'])
chi2, p, _, _ = chi2_contingency(observed)

print("T-statistic:", chi2)
print("P-Value:", p)

# accumulate the count
grouped_data = merged_step3.groupby('product_category_group')['payment_type'].value_counts().unstack().fillna(0)

# heat map
plt.figure(figsize=(12, 8))
sns.heatmap(grouped_data, annot=True, cmap="YlGnBu")
plt.title('Relationship between Payment Types and Product Categories')
plt.xlabel('Payment Type')
plt.ylabel('Product Category')
plt.show()
