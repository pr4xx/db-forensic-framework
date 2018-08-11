from framework.analysis.Export import Export


class PurchasesHtml(Export):

    def to_file(self, output_path, result_json):
        with open('framework/analysis/purchases/html/template.html', 'r') as template:
            template_string = template.read()
        export_string = template_string.replace("'<placeholder>'", result_json)
        with open(output_path, 'w') as output_file:
            output_file.write(export_string)