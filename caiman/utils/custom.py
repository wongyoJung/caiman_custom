import json


def saveIndividuals(coordinates,dFs,filename):
    cells={}
    id=0
    for c in coordinates:
        #cell={"x":[],"y":[],"dF":[]}
        cell={"cnt":[],"dF":[]}
    
        coords = []
        dF=[]
        cnts = c['coordinates']

        for cnt in cnts:
            coords.append((cnt[0],cnt[1]))
        #cell["x"]=x
        #cell["y"]=y
        #cell["dF"]=dFs[id].tolist()
        cell["cnt"]=coords
        cell["dF"]=dFs[id].tolist()
        #cell = individualCell(x,y)
        cells[str(id)]=cell
        id=id+1
    # print(type(cells))
    # print(cells)
    with open(filename+".json","w") as f:
        json.dump(cells,f)

    return(cells)






