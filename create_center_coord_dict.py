import pickle
routes_data = pickle.load(open("routes_data.pickle","rb"))




routes_data['dag 1'] = routes_data.pop('dag_1')
routes_data['dag 2'] = routes_data.pop('dag_2')
routes_data['dag 3'] = routes_data.pop('dag_3')
routes_data['dag 4 kort'] = routes_data.pop('dag_4_kort')
routes_data['dag 4 lang'] = routes_data.pop('dag_4_lang')
routes_data['dag 5'] = routes_data.pop('dag_5')
routes_data['dag 6'] = routes_data.pop('dag_6')


print(routes_data)


pickle_out = open("routes_data_new.pickle","wb")
pickle.dump(routes_data,pickle_out)
pickle_out.close()


#route_center_coords = dict()

#route_center_coords['dag_1'] = [routes_data['dag_1'][int((len(routes_data['dag_1']))/2-1)],routes_data['dag_1'][int((len(routes_data['dag_1']))/2-2)]]
#route_center_coords['dag_2'] = [routes_data['dag_2'][int((len(routes_data['dag_2']))/2-1)],routes_data['dag_2'][int((len(routes_data['dag_2']))/2-2)]]
#route_center_coords['dag_3'] = [routes_data['dag_3'][int((len(routes_data['dag_3']))/2-1)],routes_data['dag_3'][int((len(routes_data['dag_3']))/2-2)]]
#route_center_coords['dag_4_kort'] = [routes_data['dag_4_kort'][int((len(routes_data['dag_4_kort']))/2)],routes_data['dag_4_kort'][int((len(routes_data['dag_4_kort']))/2-1)]]
#route_center_coords['dag_4_lang'] = [routes_data['dag_4_lang'][int((len(routes_data['dag_4_lang']))/2-1)],routes_data['dag_4_lang'][int((len(routes_data['dag_4_lang']))/2-2)]]
#route_center_coords['dag_5'] = [routes_data['dag_5'][int((len(routes_data['dag_5']))/2)],routes_data['dag_5'][int((len(routes_data['dag_5']))/2-1)]]
#route_center_coords['dag_6'] = [routes_data['dag_6'][int((len(routes_data['dag_6']))/2)],routes_data['dag_6'][int((len(routes_data['dag_6']))/2-1)]]



#print(route_center_coords)

#pickle_out = open("route_center_coords.pickle","wb")
#pickle.dump(route_center_coords,pickle_out)
#pickle_out.close()
