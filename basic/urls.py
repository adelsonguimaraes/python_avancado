from rest_framework.routers import DefaultRouter
from basic import viewsets

router = DefaultRouter()
router.register('zone', viewsets.ZoneModelViewSet)
router.register('marital_status', viewsets.MaritalStatusModelViewSet)
router.register('department', viewsets.DepartmentModelViewSet)
router.register('state', viewsets.StateModelViewSet)
router.register('department', viewsets.DepartmentModelViewSet)
router.register('supplier', viewsets.SupplierModelViewSet)
router.register('product_group', viewsets.ProductGroupModelViewSet)
router.register('employee', viewsets.EmployeeModelViewSet)
router.register('sale', viewsets.SaleModelViewSet)
router.register('product', viewsets.ProductModelViewSet)
router.register('branch', viewsets.BranchModelViewSet)


urlpatterns = router.urls
