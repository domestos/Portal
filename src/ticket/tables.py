import django_tables2 as tables
from .models import Ticket
from django_tables2_column_shifter.tables import ColumnShiftTable
from django_tables2.utils import A  # alias for Accessor
        
class PersonTable(tables.Table):
    id = tables.LinkColumn("detail_ticket", args=[A("pk")])
    priority = tables.Column(attrs={"td": {"class": "text-danger"}})
    subject = tables.Column(attrs={"td": {"background": "red"}})
    class Meta:
        model = Ticket
        template_name = 'django_tables2/bootstrap4.html'
        fields = ('id','created','modified','created_by','cc','subject','progress', 'priority','due_date')
