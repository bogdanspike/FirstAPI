import csv

from flask import Flask, request

app = Flask(__name__)


def get_data():
    csv_file_path = 'fci-breeds.csv'
    list_of_json_obj = []
    is_first_row = True
    with open(csv_file_path) as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if is_first_row:
                is_first_row = False
            else:
                json_obj = create_json_from_array(row)
                list_of_json_obj.append(json_obj)
    return list_of_json_obj


def create_json_from_array(list_of_elem):
    return {
        list_of_elem[0]: {
            'name': list_of_elem[1],
            'section': list_of_elem[2],
            'provisional': list_of_elem[3],
            'country': list_of_elem[4],
            'url': list_of_elem[5],
            'image': list_of_elem[6],
            'pdf': list_of_elem[7]
        }
    }


def get_only_one_column(column_name):
    list_of_json_obj = get_data()
    new_list_of_json_obj = []
    for json_obj in list_of_json_obj:
        key, value = list(json_obj.items())[0]
        new_json_obj = {
            key: {
                'name': value.get('name'),
                column_name: value.get(column_name)
        }
        }
        new_list_of_json_obj.append(new_json_obj)
    return new_list_of_json_obj


@app.route("/home")
def hello():
    return "Welcome to Summoners Rift!", 200


@app.route("/dog-list", methods=['GET', 'POST'])
def dog_list():
    if request.method == 'GET':
        list_of_json_obj = get_data()
        return {
            'result': list_of_json_obj
               }, 200

    elif request.method == 'POST':
        my_dict_data = request.json
        column_name = my_dict_data.get('column_name', None)
        my_list_of_json_obj = get_only_one_column(column_name)
        return {
            'result': my_list_of_json_obj
               }, 200


if __name__ == '__main__':
    app.run(debug=True)

