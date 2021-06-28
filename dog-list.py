import csv
from pprint import pprint

from flask import Flask, request

app = Flask(__name__)


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


class DataStore:

    def __init__(self):
        self.data = DataStore.get_original_data()

    def get_data(self):
        return self.data

    def find_and_replace(self, breed_id, column_name, new_value):
        for i in range(0, len(self.data) - 1):
            key, value = list(self.data[i].items())[0]
            if key == breed_id:
                self.data[i][breed_id][column_name] = new_value

    def max_value_of_ids(self):
        global new_id_str, new_id, i
        new_list = []
        for i in range(0, len(self.data)):
            for j in self.data[i].keys():
                new_list.append(int(j))
            max_id = max(new_list)
            new_id = max_id + 1
        new_id_str = str(new_id)
        new_list.append(new_id_str)
        return new_id_str

    def add_breed(self, breed_data):
        empty_dict = {
            ds.max_value_of_ids():
                {
                    'country': None,
                    'image': None,
                    'name': None,
                    'pdf': None,
                    'provisional': None,
                    'section': None,
                    'url': None,
                }
        }
        empty_dict[ds.max_value_of_ids()].update(breed_data)
        self.data.append(empty_dict)
        return self.data



    def update_breed(self, new_breed_data):
        listed_dict = ['id', 'name', 'section', 'provisional', 'country', 'url', 'image', 'pdf']
        requested_dict = list(new_breed_data.keys())
        k=1
        for i in range(len(listed_dict)):
            if len(listed_dict) == len(requested_dict) and listed_dict[i] == requested_dict[i]:
                for i in range(0, len(self.data)):
                    key, value = list(self.data[i].items())[0]
                    if key == new_breed_data['id']:
                        self.data[i][key].update(new_breed_data)
            else:
                k=0
        return k


    @staticmethod
    def get_original_data():
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


ds = DataStore()


def get_only_one_column(column_name):
    list_of_json_obj = ds.get_data()
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
        list_of_json_obj = ds.get_data()
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


@app.route("/update-dog-list", methods=['PATCH', 'POST', 'PUT'])
def update_dog_list():
    if request.method == 'PATCH':
        my_dict_data = request.json
        breed_id = my_dict_data['id']
        column_name = list(my_dict_data.keys())[1]
        new_value = my_dict_data[column_name]
        ds.find_and_replace(breed_id, column_name, new_value)
        return {
                   'result': 'success'
               }, 200

    elif request.method == 'POST':
        if request.json == None:
            return {
                'Nu a fost introdus nimic'
            }, 204
        ds.add_breed(request.json)
        return {
                   'result': 'success'
               }, 200

    elif request.method == 'PUT':
        if ds.update_breed(request.json):
            return {
                   'result': 'success'
               }, 200
        else:
            return {
                'result': 'request failed'
            }, 400


@app.route("/delete-dog-breed", methods=['DELETE'])
def delete_dog_breed():
    if request.method == 'DELETE':
        # if type(json)
        pass


if __name__ == '__main__':
    app.run(debug=True)
