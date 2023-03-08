from rest_framework import viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.templatetags.rest_framework import data
from rest_framework_simplejwt.authentication import JWTAuthentication

# from rest_framework_simplejwt import JWTAuthentication

from .models import Company, CompanyBank, Medicine, MedicalDetails, Employee, Customer, Bill, EmployeeSalary, \
    BillDetail, CustomerRequest, CompanyAccount, EmployeeBank
from .serializer import CompanySerializer, CompanyBankSerializer, MedicineSerializer, MedicalDetailsSerializer, \
    EmployeeSerializer, CustomerSerializer, BillSerializer, EmployeeSalarySerializer, BillDetailSerializer, \
    CustomerRequestSerializer, CompanyAccountSerializer, EmployeeBankSerializer, MedicalDetailsSerializerSimple


# Create your views here.

# CompanyAPI

class CompanyViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        company = Company.objects.all()
        serializer = CompanySerializer(company, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Company List Data", "date": serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer = CompanySerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Company Data is Store Successfully"}
        except:
            dict_response = {"error": True, "message": "Error during saving company data"}

        return Response(dict_response)

    def update(self, request, pk=None):
        try:
            queryset = Company.objects.all()
            company = get_object_or_404(queryset, pk=pk)
            serializer = CompanySerializer(company, data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Company Data is Update Successfully"}
        except:
            dict_response = {"error": True, "message": "Error during saving company data"}

        return Response(dict_response)


# CompanyBank API
class CompanyBankViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            serializer = CompanyBankSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Company Bank Data is Store Successfully"}
        except:
            dict_response = {"error": True, "message": "Error during saving Company Bank data"}

        return Response(dict_response)

    def list(self, request):
        companybank = CompanyBank.objects.all()
        serializer = CompanyBankSerializer(companybank, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Company bank List Data", "date": serializer.data}
        return Response(response_dict)

    def retrieve(self, request, pk=None):
        queryset = CompanyBank.objects.all()
        companybank = get_object_or_404(queryset, pk=pk)
        serializer = CompanyBankSerializer(companybank, context={"request": request})
        return Response({"error": False, "message": "single date fetch", "data": serializer.data})

    def update(self, request, pk=None):
        queryset = CompanyBank.objects.all()
        companybank = get_object_or_404(queryset, pk=pk)
        serializer = CompanyBankSerializer(companybank, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"error": False, "message": "Data has been updateed"})


class CompanyNameViewSet(generics.ListAPIView):
    serializer_class = CompanySerializer

    def get_queryset(self):
        name = self.kwargs["name"]
        return Company.objects.filter(name=name)


# Medicine API

class MedicineViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            serializer = MedicineSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            medicine_id = serializer.data['id'];
            # Access the serilizer id Which just save in the database
            # print(medicine_id)

            # adding and saving id into medicine details table
            medicine_detail_list = []
            for medicine_detail in request.data["medicine_details"]:
                # print(medicine_detail)

                # adding medicine_id which will work for medicine_details serializer
                medicine_detail["medicine_id"] = medicine_id
                medicine_detail_list.append(medicine_detail)
                print(medicine_detail)

            serializer2 = MedicalDetailsSerializer(data=medicine_detail_list, many=True, context={"request": request})
            serializer2.is_valid()
            serializer2.save()

            dict_response = {"error": False, "message": "Medicine Data is Store Successfully"}
        except:
            dict_response = {"error": True, "message": "Error during saving Medicine data"}

        return Response(dict_response)

    def list(self, request):
        medicine = Medicine.objects.all()
        serializer = MedicineSerializer(medicine, many=True, context={"request": request})

        medicine_data = serializer.data

        newmedicainelist = []

        # adding extra key for medical detail in medicine
        for medicine in medicine_data:
            #     accessing all the medicine details of current medicine ID
            medicine_details = MedicalDetails.objects.filter(medicine_id=medicine["id"])
            medicine_details_serializers = MedicalDetailsSerializerSimple(medicine_details, many=True)
            medicine["medicine_details"] = medicine_details_serializers.data
            newmedicainelist.append(medicine)

        response_dict = {"error": False, "message": "All Medicine List Data", "date": newmedicainelist}
        return Response(response_dict)

    def retrieve(self, request, pk=None):
        queryset = Medicine.objects.all()
        medicine = get_object_or_404(queryset, pk=pk)
        serializer = MedicineSerializer(medicine, context={"request": request})

        serializer_data=serializer.data
        # accessing all the medicine details of current medicine ID
        medicine_details = MedicalDetails.objects.filter(medicine_id=serializer_data["id"])
        medicine_details_serializers = MedicalDetailsSerializerSimple(medicine_details, many=True)
        serializer_data["medicine_details"] = medicine_details_serializers.data

        return Response({"error": False, "message": "single date fetch", "data": serializer_data})

    def update(self, request, pk=None):
        queryset = Medicine.objects.all()
        medicine = get_object_or_404(queryset, pk=pk)
        serializer = MedicineSerializer(medicine, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"error": False, "message": "Data has been updateed"})


# # MedicalDetailsAPI'
# class MedicalDetailsViewSet(viewsets.ViewSet):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def create(self, request):
#         try:
#             serializer = MedicalDetailsSerializer(data=request.data, context={"request": request})
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             dict_response = {"error": False, "message": "Company Bank Data is Store Successfully"}
#         except:
#             dict_response = {"error": True, "message": "Error during saving Company Bank data"}
#
#         return Response(dict_response)
#
#     def list(self, request):
#         medicinedetail = MedicalDetails.objects.all()
#         serializer = MedicalDetailsSerializer(medicinedetail, many=True, context={"request": request})
#         response_dict = {"error": False, "message": "All Company bank List Data", "date": serializer.data}
#         return Response(response_dict)
#
#     def retrieve(self, request, pk=None):
#         queryset = MedicalDetails.objects.all()
#         medicinedetail = get_object_or_404(queryset, pk=pk)
#         serializer = MedicalDetailsSerializer(medicinedetail, context={"request": request})
#         return Response({"error": False, "message": "single date fetch", "data": serializer.data})
#
#     def update(self, request, pk=None):
#         queryset = MedicalDetails.objects.all()
#         medicinedetail = get_object_or_404(queryset, pk=pk)
#         serializer = MedicalDetailsSerializer(medicinedetail, data=request.data, context={"request": request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"error": False, "message": "Data has been updateed"})
#
#
# # EmployeeAPI
# class EmployeeViewSet(viewsets.ViewSet):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def create(self, request):
#         try:
#             serializer = EmployeeSerializer(data=request.data, context={"request": request})
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             dict_response = {"error": False, "message": "Company Bank Data is Store Successfully"}
#         except:
#             dict_response = {"error": True, "message": "Error during saving Company Bank data"}
#
#         return Response(dict_response)
#
#     def list(self, request):
#         employee = Employee.objects.all()
#         serializer = EmployeeSerializer(employee, many=True, context={"request": request})
#         response_dict = {"error": False, "message": "All Company bank List Data", "date": serializer.data}
#         return Response(response_dict)
#
#     def retrieve(self, request, pk=None):
#         queryset = Employee.objects.all()
#         employee = get_object_or_404(queryset, pk=pk)
#         serializer = EmployeeSerializer(employee, context={"request": request})
#         return Response({"error": False, "message": "single date fetch", "data": serializer.data})
#
#     def update(self, request, pk=None):
#         queryset = Employee.objects.all()
#         employee = get_object_or_404(queryset, pk=pk)
#         serializer = EmployeeSerializer(employee, data=request.data, context={"request": request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"error": False, "message": "Data has been updateed"})
#
# # CustomerAPI
# class CustomerViewSet(viewsets.ViewSet):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def create(self, request):
#         try:
#             serializer = CustomerSerializer(data=request.data, context={"request": request})
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             dict_response = {"error": False, "message": "Company Bank Data is Store Successfully"}
#         except:
#             dict_response = {"error": True, "message": "Error during saving Company Bank data"}
#
#         return Response(dict_response)
#
#     def list(self, request):
#         customer = Customer.objects.all()
#         serializer = CustomerSerializer(customer, many=True, context={"request": request})
#         response_dict = {"error": False, "message": "All Company bank List Data", "date": serializer.data}
#         return Response(response_dict)
#
#     def retrieve(self, request, pk=None):
#         queryset = Customer.objects.all()
#         customer = get_object_or_404(queryset, pk=pk)
#         serializer = CustomerSerializer(customer, context={"request": request})
#         return Response({"error": False, "message": "single date fetch", "data": serializer.data})
#
#     def update(self, request, pk=None):
#         queryset = Customer.objects.all()
#         customer = get_object_or_404(queryset, pk=pk)
#         serializer = CustomerSerializer(customer, data=request.data, context={"request": request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"error": False, "message": "Data has been updateed"})
# # BillAPI
# class BillViewSet(viewsets.ViewSet):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def create(self, request):
#         try:
#             serializer = BillSerializer(data=request.data, context={"request": request})
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             dict_response = {"error": False, "message": "Company Bank Data is Store Successfully"}
#         except:
#             dict_response = {"error": True, "message": "Error during saving Company Bank data"}
#
#         return Response(dict_response)
#
#     def list(self, request):
#         bill = Bill.objects.all()
#         serializer = BillSerializer(bill, many=True, context={"request": request})
#         response_dict = {"error": False, "message": "All Company bank List Data", "date": serializer.data}
#         return Response(response_dict)
#
#     def retrieve(self, request, pk=None):
#         queryset = Bill.objects.all()
#         bill = get_object_or_404(queryset, pk=pk)
#         serializer = BillSerializer(bill, context={"request": request})
#         return Response({"error": False, "message": "single date fetch", "data": serializer.data})
#
#     def update(self, request, pk=None):
#         queryset = Bill.objects.all()
#         bill = get_object_or_404(queryset, pk=pk)
#         serializer = BillSerializer(bill, data=request.data, context={"request": request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"error": False, "message": "Data has been updateed"})
#
# # EmployeeSalaryAPI
# class EmployeeSalaryViewSet(viewsets.ViewSet):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def create(self, request):
#         try:
#             serializer = EmployeeSalarySerializer(data=request.data, context={"request": request})
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             dict_response = {"error": False, "message": "Company Bank Data is Store Successfully"}
#         except:
#             dict_response = {"error": True, "message": "Error during saving Company Bank data"}
#
#         return Response(dict_response)
#
#     def list(self, request):
#         employeesalary = EmployeeSalary.objects.all()
#         serializer = EmployeeSalarySerializer(employeesalary, many=True, context={"request": request})
#         response_dict = {"error": False, "message": "All Company bank List Data", "date": serializer.data}
#         return Response(response_dict)
#
#     def retrieve(self, request, pk=None):
#         queryset = EmployeeSalary.objects.all()
#         employeesalary = get_object_or_404(queryset, pk=pk)
#         serializer = EmployeeSalarySerializer(employeesalary, context={"request": request})
#         return Response({"error": False, "message": "single date fetch", "data": serializer.data})
#
#     def update(self, request, pk=None):
#         queryset = EmployeeSalary.objects.all()
#         employeesalary = get_object_or_404(queryset, pk=pk)
#         serializer = EmployeeSalarySerializer(employeesalary, data=request.data, context={"request": request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"error": False, "message": "Data has been updateed"})
# # BillDetailAPI
# class BillDetailViewSet(viewsets.ViewSet):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def create(self, request):
#         try:
#             serializer = BillDetailSerializer(data=request.data, context={"request": request})
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             dict_response = {"error": False, "message": "Company Bank Data is Store Successfully"}
#         except:
#             dict_response = {"error": True, "message": "Error during saving Company Bank data"}
#
#         return Response(dict_response)
#
#     def list(self, request):
#         billdetail = BillDetail.objects.all()
#         serializer = BillDetailSerializer(billdetail, many=True, context={"request": request})
#         response_dict = {"error": False, "message": "All Company bank List Data", "date": serializer.data}
#         return Response(response_dict)
#
#     def retrieve(self, request, pk=None):
#         queryset = BillDetail.objects.all()
#         billdetail = get_object_or_404(queryset, pk=pk)
#         serializer = BillDetailSerializer(billdetail, context={"request": request})
#         return Response({"error": False, "message": "single date fetch", "data": serializer.data})
#
#     def update(self, request, pk=None):
#         queryset = BillDetail.objects.all()
#         billdetail = get_object_or_404(queryset, pk=pk)
#         serializer = BillDetailSerializer(billdetail, data=request.data, context={"request": request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"error": False, "message": "Data has been updateed"})
# # CustomerRequestAPI
# class CustomerRequestViewSet(viewsets.ViewSet):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def create(self, request):
#         try:
#             serializer = CustomerRequestSerializer(data=request.data, context={"request": request})
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             dict_response = {"error": False, "message": "Company Bank Data is Store Successfully"}
#         except:
#             dict_response = {"error": True, "message": "Error during saving Company Bank data"}
#
#         return Response(dict_response)
#
#     def list(self, request):
#         customerrequest = CustomerRequest.objects.all()
#         serializer = CustomerRequestSerializer(customerrequest, many=True, context={"request": request})
#         response_dict = {"error": False, "message": "All Company bank List Data", "date": serializer.data}
#         return Response(response_dict)
#
#     def retrieve(self, request, pk=None):
#         queryset = CustomerRequest.objects.all()
#         customerrequest = get_object_or_404(queryset, pk=pk)
#         serializer = CustomerRequestSerializer(customerrequest, context={"request": request})
#         return Response({"error": False, "message": "single date fetch", "data": serializer.data})
#
#     def update(self, request, pk=None):
#         queryset = CustomerRequest.objects.all()
#         customerrequest = get_object_or_404(queryset, pk=pk)
#         serializer = CustomerRequestSerializer(customerrequest, data=request.data, context={"request": request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"error": False, "message": "Data has been updateed"})
# # CompanyAccountAPI
# class EmployeeViewSet(viewsets.ViewSet):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def create(self, request):
#         try:
#             serializer = CompanyAccountSerializer(data=request.data, context={"request": request})
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             dict_response = {"error": False, "message": "Company Bank Data is Store Successfully"}
#         except:
#             dict_response = {"error": True, "message": "Error during saving Company Bank data"}
#
#         return Response(dict_response)
#
#     def list(self, request):
#         companyaccount = CompanyAccount.objects.all()
#         serializer = CompanyAccountSerializer(companyaccount, many=True, context={"request": request})
#         response_dict = {"error": False, "message": "All Company bank List Data", "date": serializer.data}
#         return Response(response_dict)
#
#     def retrieve(self, request, pk=None):
#         queryset = CompanyAccount.objects.all()
#         companyaccount = get_object_or_404(queryset, pk=pk)
#         serializer = CompanyAccountSerializer(companyaccount, context={"request": request})
#         return Response({"error": False, "message": "single date fetch", "data": serializer.data})
#
#     def update(self, request, pk=None):
#         queryset = CompanyAccount.objects.all()
#         companyaccount = get_object_or_404(queryset, pk=pk)
#         serializer = CompanyAccountSerializer(companyaccount, data=request.data, context={"request": request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"error": False, "message": "Data has been updateed"})
# # EmployeeBankAPI
# class EmployeeBankViewSet(viewsets.ViewSet):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def create(self, request):
#         try:
#             serializer = EmployeeBankSerializer(data=request.data, context={"request": request})
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             dict_response = {"error": False, "message": "Company Bank Data is Store Successfully"}
#         except:
#             dict_response = {"error": True, "message": "Error during saving Company Bank data"}
#
#         return Response(dict_response)
#
#     def list(self, request):
#         employeebank = EmployeeBank.objects.all()
#         serializer = EmployeeBankSerializer(employeebank, many=True, context={"request": request})
#         response_dict = {"error": False, "message": "All Company bank List Data", "date": serializer.data}
#         return Response(response_dict)
#
#     def retrieve(self, request, pk=None):
#         queryset = EmployeeBank.objects.all()
#         employeebank = get_object_or_404(queryset, pk=pk)
#         serializer = EmployeeBankSerializer(employeebank, context={"request": request})
#         return Response({"error": False, "message": "single date fetch", "data": serializer.data})
#
#     def update(self, request, pk=None):
#         queryset = EmployeeBank.objects.all()
#         employeebank = get_object_or_404(queryset, pk=pk)
#         serializer = EmployeeBankSerializer(employeebank, data=request.data, context={"request": request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"error": False, "message": "Data has been updateed"})


company_list = CompanyViewSet.as_view({"get": "list"})
company_create = CompanyViewSet.as_view({"post": "create"})
company_update = CompanyViewSet.as_view({"put": "update"})
