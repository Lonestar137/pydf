import pdfrw
from rich.console import Console

def get_form_field_names(pdf: object):
    key_dict = {}
    for page in pdf.pages:
        identifier = page['/Annots']
        for j in identifier:
            if j['/Subtype'] == '/Widget':
                try:
                    key = j['/T'][1:-1]
                    key_dict[key] = j['/V']
                except TypeError as e:
                    key = (j['/T'])
                    key_dict[key] = j['/V']
                    pass


    # Returns key, value dict for annotations in the pdf.
    return key_dict


def fill_pdf(pdf: object, form_dict: dict):
    for page in pdf.pages:
        for i in page['/Annots']:
            if i['/Subtype'] == '/Widget':
                try:
                    key = i['/T'][1:-1]
                except TypeError as e:
                    key = (i['/T'])
                if key in form_dict:
                    if type(form_dict[key]) == bool:
                        # If checkbox and value is true, set to checked.
                        if form_dict[key] == True:
                            i.update(pdfrw.PdfDict(AS=pdfrw.PdfName('Yes'))) 
                    else:
                        i.update(pdfrw.PdfDict(AP=""))
                        i.update(pdfrw.PdfDict(V=form_dict[key]))
                        i.update(pdfrw.PdfDict(AS=form_dict[key]))

    # TODO  - Writes to <date>.pdf 
    pdfrw.PdfWriter().write('filled_form.pdf', pdf)

def print_values(form_fields):
    #Colored text output for viewing fields
    console = Console()

    #See available fields.
    #print(form_fields)
    for key, value in form_fields.items():
        console.print(f'{key}: [not bold]{value}[/not bold]', style='bold')


#Read pdf create dict
pdf_template = pdfrw.PdfReader('Example.pdf')
pdf_template.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject("true")))
form_fields = get_form_field_names(pdf_template)



#Assign values
form_fields['Pay Period'] = 'Feb 1-15 2022'
form_fields['Employee Name'] = 'John Doe'
form_fields['Payroll ID'] = '98734'
form_fields['Week One Total Hours Worked'] = '40'
form_fields['Current Pay Period Total Hours'] = '40'
form_fields['Date/Tuesday \(Week One\)'] = '(10/17/2018)'
form_fields['Date/Tuesday \(Week One\)'] = '(10/17/2018)'
form_fields['Tuesday \(Week One\) Leave Used'] = '8'
form_fields['Date/Wednesday \(Week One\)'] = '(10/18/2018)'
form_fields[' \(Week One\) 1 Hour Lunch'] = True 




# Print the form fields: values extracted from given pdf.
print_values(form_fields)
fill_pdf(pdf_template, form_fields)



#TODO - Add a option to apply signature from a image file.
