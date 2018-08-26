from pony.orm import Database
from framework.ConnectionManager import ConnectionManager
from framework.DatabaseIdentifier import DatabaseIdentifier
from framework.PluginManager import PluginManager
from framework.analysis.timeline import Timeline
from framework.analysis.timeline.excel.TimelineExcel import TimelineExcel
from framework.analysis.timeline.html.TimelineHtml import TimelineHtml
from framework.analysis.chat import Chat
from framework.analysis.chat.excel.ChatExcel import ChatExcel
from framework.analysis.chat.html.ChatHtml import ChatHtml
from framework.analysis.purchases import Purchases
from framework.analysis.purchases.excel.PurchasesExcel import PurchasesExcel
from framework.analysis.purchases.html.PurchasesHtml import PurchasesHtml


class Core:

    instance = None

    def __init__(self):
        self.connection_manager = ConnectionManager(self)
        self.plugin_manager = PluginManager(self)
        self.database_identifier = DatabaseIdentifier(self)
        self.connection = None
        self.export = None
        self.output = None
        self.db = Database()
        Core.instance = self

    def init(self, connection_name, export_type, output_path):
        if connection_name is not None:
            self.connection = self.connection_manager.get_connection(connection_name)
            self.connection_manager.bind_db(self.db, connection_name)
        if export_type is not None:
            self.export = export_type
        if output_path is not None:
            self.output = output_path

    def render(self, result):
        result_json = result.to_json()

        if self.export == 'json':
            print(result_json)
            return

        exporter = None
        if isinstance(result, Timeline.Timeline):
            if self.export == 'html':
                exporter = TimelineHtml()
            if self.export == 'excel':
                exporter = TimelineExcel()
        if isinstance(result, Chat.Chat):
            if self.export == 'html':
                exporter = ChatHtml()
            if self.export == 'excel':
                exporter = ChatExcel()
        if isinstance(result, Purchases.Purchases):
            if self.export == 'html':
                exporter = PurchasesHtml()
            if self.export == 'excel':
                exporter = PurchasesExcel()
        exporter.to_file(self.output, result_json)
        print("Written " + self.output)