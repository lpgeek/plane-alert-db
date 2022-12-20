import csv
import copy

input_csv_source = 'plane-alert-MASTER-db-images.csv'
input_csv_ignore_types = ['#CMPG','#N/A']
input_master_row_inmain_num = 2
input_master_row_csv_type = 6
input_master_header = []
input_csv_seek_to = 1
output_csv_type_all = "db"
output_csv_types = [output_csv_type_all]
output_csv_written = []
output_csv_filename_base = 'plane-alert-'
output_csv_filename_images_str = '-images'
output_csv_filename_suffix = '.csv'
output_csv_list_truncate_num = 3
output_csv_file_truncate_num = 2
output_csv_list_inmain_false = 'False'
output_csv_data = []
output_csv_data_images = []
output_csv_filename = ''
output_csv_filename_image = ''

#open our master csv
with open(input_csv_source) as master_csv_obj:
    master_csv_reader = csv.reader(master_csv_obj)

    #get our header row, will be used in output later on
    master_header = next(master_csv_reader)

    #remove the "inmain" reference from the header
    master_header.pop(input_master_row_inmain_num)

    #copy the headers to be used for images (deep because we don't want to pass reference)
    master_header_images = copy.deepcopy(master_header)

    #remove the headers we don't want for not-images
    del master_header[len(master_header) - output_csv_list_truncate_num:]

    #parse the entire file for unique csv types, ignoring the ignored ones
    for master_row in master_csv_reader:
        master_csv_type = master_row[input_master_row_csv_type]
        if master_csv_type not in output_csv_types and master_csv_type not in input_csv_ignore_types:

            output_csv_types.append(master_csv_type)

    #use our established list of types to parse the master and build the csvs
    for output_csv_type in output_csv_types:
        master_csv_obj.seek(input_csv_seek_to)
        next(master_csv_reader)

        #reset our output lists
        output_csv_data = []
        output_csv_data_images = []

        #process each row
        for master_row in master_csv_reader:
            master_row_csv_type = master_row[input_master_row_csv_type]

            #if the current row is of the type we're wanting, or we're doing everything aka "db"
            if output_csv_type == output_csv_type_all or output_csv_type == master_row_csv_type: 

                #if this is all, we don't want rows which we've said "False" to "InMain"
                if not (output_csv_type == output_csv_type_all and master_row[input_master_row_inmain_num] == output_csv_list_inmain_false):

                    #remove the "inmain" reference from the row
                    master_row.pop(input_master_row_inmain_num)

                    #copy the headers to be used for images (deep because we don't want to pass reference)
                    master_row_images = copy.deepcopy(master_row)
                    output_csv_data_images.append(master_row_images)

                    #remove the entries we don't want for not-images amd add to our not-images output
                    del master_row[len(master_row) - output_csv_list_truncate_num:]
                    output_csv_data.append(master_row)

        #build some super elegant file output strings
        output_csv_filename = '{}{}{}'.format(output_csv_filename_base,output_csv_type.lower(),output_csv_filename_suffix)
        output_csv_filename_images = '{}{}{}{}'.format(output_csv_filename_base,output_csv_type.lower(),output_csv_filename_images_str,output_csv_filename_suffix)

        #TODO should be a funtion
        #open the output
        with open(output_csv_filename,'w',newline='') as file_obj_output:
            #open it as a csv object and write headers and data
            writer = csv.writer(file_obj_output)
            writer.writerow(master_header)
            writer.writerows(output_csv_data)
            #get the file size to trim the line return
            size=file_obj_output.tell()
            file_obj_output.truncate(size-output_csv_file_truncate_num)

        #comments same as last time
        with open(output_csv_filename_images,'w',newline='') as file_obj_output_images:
            writer = csv.writer(file_obj_output_images)
            writer.writerow(master_header_images)
            writer.writerows(output_csv_data_images)
            size=file_obj_output_images.tell()
            file_obj_output_images.truncate(size-output_csv_file_truncate_num)
