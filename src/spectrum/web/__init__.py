"""
Copyright 2021 Nikita Hismatov.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       https://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

"""
from enum import Enum
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conlist

from spectrum.calculations.graphs import PrimeGraph
from spectrum.calculations.groups import SporadicGroup, ClassicalGroup, ExceptionalGroup


class GroupType(Enum):  # TODO: probably should be used in all project
    ALTERNATING = 'alternating'
    CLASSICAL = 'classical'
    EXCEPTIONAL = 'exceptional'
    SPORADIC = 'sporadic'


GROUP_TYPES = {
    GroupType.ALTERNATING: [],
    GroupType.CLASSICAL: ClassicalGroup.types(),
    GroupType.EXCEPTIONAL: ExceptionalGroup.types(),
    GroupType.SPORADIC: SporadicGroup.all_groups(),
}

app = FastAPI()


@app.get('/groups/')
async def groups():
    return GROUP_TYPES


# @app.get('/groups/{group_type}/{group_name}/')  # TODO: separate method for each type, separate Enums for group_names?
# async def group_gk(group_type: GroupType, group_name: str):
#     pass


class GraphResponseModel(BaseModel):
    vertices: List[int]
    edges: List[conlist(item_type=int, min_items=2, max_items=2)]


@app.get('/groups/sporadic/{group_name}/gk/', response_model=GraphResponseModel)
async def sporadic_graph_gk(group_name: str):
    if group_name not in GROUP_TYPES[GroupType.SPORADIC]:
        raise HTTPException(status_code=404, detail="Item not found")
    g = SporadicGroup(group_name)
    graph = PrimeGraph(g)
    return {
        'vertices': graph.vertices,
        'edges': graph.edges,
    }
