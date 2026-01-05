from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo

class DemoRestApi(APIView):
    name = "Demo REST API"
    def get(self, request):

      # Filtra la lista para incluir solo los elementos donde 'is_active' es True
      active_items = [item for item in data_list if item.get('is_active', False)]
      return Response(active_items, status=status.HTTP_200_OK)

    def post(self, request):
      data = request.data

      # Validación mínima
      if 'name' not in data or 'email' not in data:
         return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

      data['id'] = str(uuid.uuid4())
      data['is_active'] = True
      data_list.append(data)

      return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)

    
class DemoRestApiItem(APIView):
    
    def get_item(self, item_id):
        for item in data_list:
            if item['id'] == item_id:
                return item
        return None

    def put(self, request, item_id):
        """
        Reemplaza completamente los datos del elemento,
        excepto el identificador.
        """
        item = self.get_item(item_id)
        if not item:
            return Response(
                {'error': 'Elemento no encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )

        data = request.data

        if 'id' not in data:
            return Response(
                {'error': 'El campo id es obligatorio.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Reemplazo total excepto el ID
        item['name'] = data.get('name')
        item['email'] = data.get('email')
        item['is_active'] = data.get('is_active', item['is_active'])

        return Response(
            {'message': 'Elemento actualizado completamente.'},
            status=status.HTTP_200_OK
        )
    
    def patch(self, request, item_id):
        """
        Actualiza parcialmente los campos del elemento.
        """
        item = self.get_item(item_id)
        if not item:
            return Response(
                {'error': 'Elemento no encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )

        data = request.data

        for field in ['name', 'email', 'is_active']:
            if field in data:
                item[field] = data[field]

        return Response(
            {'message': 'Elemento actualizado parcialmente.'},
            status=status.HTTP_200_OK
        )

    def delete(self, request, item_id):
        """
        Eliminación lógica del elemento (is_active = False).
        """
        item = self.get_item(item_id)
        if not item:
            return Response(
                {'error': 'Elemento no encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )

        item['is_active'] = False

        return Response(
            {'message': 'Elemento eliminado lógicamente.'},
            status=status.HTTP_200_OK
        )