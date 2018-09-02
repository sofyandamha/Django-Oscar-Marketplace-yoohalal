from oscar.apps.dashboard.catalogue.tables import ProductTable


class ProductTable(ProductTable):

    class Meta(ProductTable.Meta):
        fields = ProductTable.Meta.fields + ('status',)