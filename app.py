import matplotlib.pyplot as plt
import networkx as nx
import csv
        
# Creación de grafo vacío
G = nx.Graph() 

# Creación de vértices
nombreVertices = ['101', '102', '103', '104','105', 
              '201', '202', '203', '204','205',
              '301', '302', '303', '304','305',
              '401']

#Agregación de los vértices al grafo con sus atributos
select = input("Bienvenido(a) \n 1.Cargar los datos desde un archivo csv de prueba \n" 
               "2.Cargar los datos de cada nodo manualmente\n")
if select == '1':
    with open(".\datos.csv", 'r') as file:
        count = 0
        csv_file = csv.reader(file)
        for row in csv_file:
            if count < 1: count+=1
            else:
                G.add_node(row[0], tasaMetabolica=float(row[1]),indice_cl=float(row[2]),velocidadAire=float(row[3]),temperaturaAmbiente=float(row[4]),
                        temperaturaInterna=float(row[5]),materialPared=row[6],humedadAire=int(row[7]),capacidad=int(row[8]),
                        cantidadPersonas=int(row[9]),temperaturaOperativa=0,habitabilidad=False)   
                
else:
    vTemperaturaAmbiente = int(input("Ingrese la temperatura ambiente: "))
    for i in range(0,16):
        print("Habitación "+nombreVertices[i])
        vTasaMetabolica = float(input("Ingrese la tasa metabólica promedio: "))
        vIndiceCl = float(input("Ingrese el índice de aislamiento de la vestimenta promedio: "))
        vTtemperaturaInterna = int(input("Ingrese la temperatura de la habitación (Temperatura interna):"))
        material = input("Ingrese el tipo de material de la pared \n1.Ladrillo y concreto \n2.Madera\n")
        if material =='1':
            vTmaterialPared='Ladrillo y concreto'
        else:
            vMaterialPared='Madera'
        vHumedadAire = int(input("Ingrese el porcentaje de humedad del aire de la habitación: "))
        vCapacidad = int(input("Ingrese la cantidad Máxima de personas que se permite estar en la habitación: "))
        vCantidadPersonas = int(input("Ingrese la cantidad de personas que estarán en la habitación: "))
        G.add_node(nombreVertices[i],tasaMetabolica=vTasaMetabolica,indice_cl=vIndiceCl, temperaturaAmbiente=vTemperaturaAmbiente,
                   temperaturaInterna=vTtemperaturaInterna,
                   materialPared=vTmaterialPared,humedadAire=vHumedadAire,cantidadPersonas=vCapacidad,
                   capacidad=vCantidadPersonas,temperaturaOperativa=0,habitabilidad=False)   
       
            
#Creación de aristas
aristas_G = [(nombreVertices[0], nombreVertices[1]), (nombreVertices[1], nombreVertices[2]), (nombreVertices[2], nombreVertices[3]), (nombreVertices[3], nombreVertices[4]), (nombreVertices[4], nombreVertices[0]), 
             (nombreVertices[0], nombreVertices[5]), (nombreVertices[1], nombreVertices[6]), (nombreVertices[2], nombreVertices[7]), (nombreVertices[3], nombreVertices[8]), (nombreVertices[4], nombreVertices[9]),
             (nombreVertices[5], nombreVertices[6]), (nombreVertices[6], nombreVertices[7]), (nombreVertices[7], nombreVertices[8]), (nombreVertices[8], nombreVertices[9]), (nombreVertices[9], nombreVertices[5]), 
             (nombreVertices[5], nombreVertices[10]), (nombreVertices[6], nombreVertices[11]), (nombreVertices[7], nombreVertices[12]), (nombreVertices[8], nombreVertices[13]), (nombreVertices[9], nombreVertices[14]),
             (nombreVertices[10], nombreVertices[11]), (nombreVertices[11], nombreVertices[12]), (nombreVertices[12], nombreVertices[13]), (nombreVertices[13], nombreVertices[14]), (nombreVertices[14], nombreVertices[10]),
             (nombreVertices[10], nombreVertices[15]), (nombreVertices[11], nombreVertices[15]), (nombreVertices[12], nombreVertices[15]), (nombreVertices[13], nombreVertices[15]), (nombreVertices[14], nombreVertices[15]),]

#Agregación de aristas al grafo
G.add_edges_from(aristas_G)

#Se crea un diccionario para cada vertice y su ubicacion en el plano X Y
ubica = {nombreVertices[0]: (0, 3), nombreVertices[1]: (3, 0), nombreVertices[2]: (7, 0), nombreVertices[3]: (10, 3), nombreVertices[4]: (5, 6),
         nombreVertices[5]: (0, 13), nombreVertices[6]: (3, 10), nombreVertices[7]: (7, 10), nombreVertices[8]: (10, 13), nombreVertices[9]: (5, 16),
         nombreVertices[10]: (0, 23), nombreVertices[11]: (3, 20), nombreVertices[12]: (7, 20), nombreVertices[13]: (10, 23), nombreVertices[14]: (5, 26),
         nombreVertices[15]: (5,35)}

#Se crea un diccionario cada vertice y la ubicación de sus atributos en el plano X Y
ubica_atributos = {nombreVertices[0]: (0, 1), nombreVertices[1]: (3, -2), nombreVertices[2]: (7, -2), nombreVertices[3]: (10, 1), nombreVertices[4]: (5, 4),
         nombreVertices[5]: (0, 11), nombreVertices[6]: (3, 8), nombreVertices[7]: (7, 8), nombreVertices[8]: (10, 11), nombreVertices[9]: (5, 14),
         nombreVertices[10]: (0, 21), nombreVertices[11]: (3, 18), nombreVertices[12]: (7, 18), nombreVertices[13]: (10, 21), nombreVertices[14]: (5, 24),
         nombreVertices[15]: (5,37)}


#Análisis habitabilidad
def calcularVelocidadRelativa(va,m):
    velocidadRelativa = va + 0.3*(m-1)
    if velocidadRelativa <0.2:
        a=0.5
    elif velocidadRelativa >= 0.2 and velocidadRelativa <=0.6:
        a = 0.6
    else:
        a= 0.7
    return a 

def calcularTemperaturaOperativa(a,ta,tr):
    temperaturaOperativa =a*ta +(1-a)*tr
    return temperaturaOperativa

for i in nombreVertices:
    cantidadP = G.nodes[i]['cantidadPersonas']
    capacidadP = G.nodes[i]['capacidad']
    a = calcularVelocidadRelativa(G.nodes[i]['velocidadAire'],G.nodes[i]['tasaMetabolica'])
    to = calcularTemperaturaOperativa(a,G.nodes[i]['temperaturaAmbiente'],G.nodes[i]['temperaturaInterna'])
    G.nodes[i]['temperaturaOperativa']=to
    if cantidadP<=capacidadP:
        if to >=20 and to<=24:
            G.nodes[i]['habitabilidad']=True
    else:
        pass

node_attributes={n:(d["temperaturaOperativa"],
                   d["humedadAire"],d["cantidadPersonas"],d["capacidad"]) for n,d in G.nodes(data=True)}

    
color_map = nx.get_node_attributes(G,'habitabilidad')
for key in color_map:
    if color_map[key]==False:
        color_map[key]="red"
    else:
        color_map[key]="green"

habitability_color = [color_map.get(node) for node in G.nodes()]   

   
# se dibuja el grafo
nx.draw(G, pos=ubica, node_color=habitability_color, with_labels=True, node_size=700,
        font_color="white",font_family="Arial",width=2)
nx.draw_networkx_labels(G,pos=ubica_atributos,labels=node_attributes)
plt.show()

















 
