from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from .decorators import vendor_or_admin_required
from django.views import View
from django.views.generic import (
    TemplateView, ListView, DetailView, UpdateView, DeleteView,
    CreateView
)

from src.accounts.decorators import admin_protected
from src.accounts.models import User
from src.administration.admins.bll import fake_data
from src.administration.admins.filters import UserFilter, ProductFilter, OrderFilter, PostFilter
from src.administration.admins.forms import ProductVersionForm, ProductImageForm, MyProfileForm, ProductPlatformForm
from src.administration.admins.models import Category, PostCategory, Product, ProductVersion, ProductImage, Order, Post, \
    Language, OtherPlatform

""" MAIN """

@method_decorator(vendor_or_admin_required, name='dispatch')

@method_decorator(vendor_or_admin_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'admins/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        fake_data()
        context['blogs'] = Post.objects.count()
        context['orders'] = Order.objects.count()
        context['users'] = User.objects.filter(is_staff=False).count()
        context['novels'] = Product.objects.count()
        return context


@method_decorator(vendor_or_admin_required, name='dispatch')
class UserOwnUpdateView(View):
    def get(self, request):
        form = MyProfileForm(instance=request.user)
        context = {'form': form}
        return render(request, template_name='admins/my-profile-change.html', context=context)

    def post(self, request):
        form = MyProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            messages.success(request, "Your profile updated successfully")
            form.save(commit=True)
        context = {'form': form}
        return render(request, template_name='admins/my-profile-change.html', context=context)


@method_decorator(vendor_or_admin_required, name='dispatch')
class UserOwnPasswordChangeView(View):

    def get(self, request):
        form = PasswordChangeForm(request.user)
        context = {'form': form}
        return render(request, template_name='admins/my-password-change.html', context=context)

    def post(self, request):
        form = PasswordChangeForm(user=request.user, data=request.POST or None)
        if form.is_valid():
            messages.success(request, "Your password changed successfully")
            form.save(commit=True)
        context = {'form': form}
        return render(request, template_name='admins/my-password-change.html', context=context)


""" USER MGMT"""


@method_decorator(vendor_or_admin_required, name='dispatch')
class UserListView(ListView):
    queryset = User.objects.all()
    template_name = 'admins/user_list.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        _filter = UserFilter(self.request.GET, queryset=User.objects.filter())
        context['filter_form'] = _filter.form

        paginator = Paginator(_filter.qs, 50)
        page_number = self.request.GET.get('page')
        page_object = paginator.get_page(page_number)

        context['object_list'] = page_object
        return context


@method_decorator(vendor_or_admin_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ['profile_image', 'first_name', 'last_name', 'email', 'username', 'is_staff', 'is_client', 'is_active']
    template_name = 'admins/user_form.html'
    success_url = reverse_lazy('admins:user-list')

    def get_success_url(self):
        return reverse_lazy('admins:user-detail', args=(self.object.pk,))


@method_decorator(vendor_or_admin_required, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ['profile_image', 'first_name', 'last_name', 'email', 'username', 'is_active']
    template_name = 'admins/user_form.html'
    success_url = reverse_lazy('admins:user-list')

    def get_success_url(self):
        return reverse_lazy('admins:user-detail', args=(self.object.pk,))


@method_decorator(vendor_or_admin_required, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    template_name = 'admins/user_confirm_delete.html'
    success_url = reverse_lazy('admins:user-list')


@method_decorator(vendor_or_admin_required, name='dispatch')
class UserDetailView(DetailView):
    model = User
    template_name = 'admins/user_detail.html'


@method_decorator(vendor_or_admin_required, name='dispatch')
class UserPasswordResetView(View):
    model = User
    template_name = 'admins/user_password_change.html'
    success_url = reverse_lazy('admins:user-list')
    context = {}

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = AdminPasswordChangeForm(user=user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = AdminPasswordChangeForm(data=request.POST, user=user)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, f"{user.get_full_name()}'s password changed successfully.")
            return redirect('admins:user-detail', user.pk)

        return render(request, self.template_name, {'form': form})


""" MANAGEMENT """


@method_decorator(vendor_or_admin_required, name='dispatch')
class CategoryListView(ListView):
    queryset = Category.objects.all()


@method_decorator(vendor_or_admin_required, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name', 'is_active']
    success_url = reverse_lazy('admins:category-list')


@method_decorator(vendor_or_admin_required, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name', 'is_active']
    success_url = reverse_lazy('admins:category-list')


@method_decorator(vendor_or_admin_required, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('admins:category-list')


@method_decorator(vendor_or_admin_required, name='dispatch')
class LanguageListView(ListView):
    queryset = Language.objects.all()


@method_decorator(vendor_or_admin_required, name='dispatch')
class LanguageUpdateView(UpdateView):
    model = Language
    fields = ['name']
    success_url = reverse_lazy('admins:category-list')


@method_decorator(vendor_or_admin_required, name='dispatch')
class LanguageCreateView(CreateView):
    model = Language
    fields = ['name']
    success_url = reverse_lazy('admins:category-list')


@method_decorator(vendor_or_admin_required, name='dispatch')
class LanguageDeleteView(DeleteView):
    model = Language
    success_url = reverse_lazy('admins:category-list')


@method_decorator(vendor_or_admin_required, name='dispatch')
class PostCategoryListView(ListView):
    queryset = PostCategory.objects.all()


@method_decorator(vendor_or_admin_required, name='dispatch')
class PostCategoryUpdateView(UpdateView):
    model = PostCategory
    fields = ['name', 'parent', 'is_active']
    success_url = reverse_lazy('admins:post-category-list')


@method_decorator(vendor_or_admin_required, name='dispatch')
class PostCategoryCreateView(CreateView):
    model = PostCategory
    fields = ['name', 'parent', 'is_active']
    success_url = reverse_lazy('admins:post-category-list')


@method_decorator(vendor_or_admin_required, name='dispatch')
class PostCategoryDeleteView(DeleteView):
    model = PostCategory
    success_url = reverse_lazy('admins:post-category-list')


""" INVENTORY """


@method_decorator(vendor_or_admin_required, name='dispatch')
class ProductListView(ListView):
    paginate_by = 16

    def get_queryset(self):
        """
        Return the products that belong to the seller profile of the logged-in user.
        """
        user = self.request.user
        if not hasattr(user, 'vendor_profile'):
            # Handle case where user doesn't have a SellerProfile
            return Product.objects.none()  # Return an empty queryset if no SellerProfile

        seller_profile = user.vendor_profile
        return Product.objects.filter(seller=seller_profile)  # Assuming `seller` is the ForeignKey in Product model

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _filter = ProductFilter(self.request.GET, queryset=self.get_queryset())
        context['filter_form'] = _filter.form

        paginator = Paginator(_filter.qs, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_object = paginator.get_page(page_number)

        context['object_list'] = page_object
        return context


@method_decorator(vendor_or_admin_required, name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    fields = [
        'thumbnail_image', 'book_file', 'name',
        'book_type', 'categories', 'languages', 'pages',
        'artist', 'author', 'translator', 'illustrator',
        'description', 'is_active'
    ]
    success_url = reverse_lazy('admins:product-list')


from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Product
from .forms import ProductForm
from src.administration.seller.models import SellerProfile
@method_decorator(vendor_or_admin_required, name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    fields = [
        'thumbnail_image', 'book_file', 'name',
        'book_type', 'categories', 'languages', 'pages',
        'artist', 'author', 'translator', 'illustrator',
        'description', 'is_active',
    ]
    success_url = reverse_lazy('admins:product-list')
    success_url = reverse_lazy('admins:product-list')  # Adjust the URL to your needs

    def form_valid(self, form):
        # Access the SellerProfile through the related_name `vendor_profile`
        try:
            seller_profile = self.request.user.vendor_profile
            form.instance.seller = seller_profile
        except SellerProfile.DoesNotExist:
            # Handle the case where the user does not have a SellerProfile
            # For example, you might redirect them with an error message
            form.add_error(None, "You must have a seller profile to create a product.")
            return super().form_invalid(form)

        return super().form_valid(form)


@method_decorator(vendor_or_admin_required, name='dispatch')
class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        product_version_forms = []
        for obj in self.object.get_versions():
            product_version_forms.append(ProductVersionForm(instance=obj))

        context['product_version_add_form'] = ProductVersionForm()
        context['product_image_add_form'] = ProductImageForm()
        context['platform_form'] = ProductPlatformForm()
        context['product_version_forms'] = product_version_forms
        return context


@method_decorator(vendor_or_admin_required, name='dispatch')
class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('admins:product-list')


@method_decorator(vendor_or_admin_required, name='dispatch')
class ProductVersionAddView(View):

    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        form = ProductVersionForm(request.POST)
        if form.is_valid():
            form.instance.product = product
            form.save()
            messages.success(request, "Product Version added successfully")
        return redirect("admins:product-detail", product_id)


@method_decorator(vendor_or_admin_required, name='dispatch')
class ProductVersionUpdateView(View):

    def post(self, request, product_id, pk):
        product = get_object_or_404(Product, pk=product_id)
        product_version = get_object_or_404(ProductVersion.objects.filter(product=product), pk=pk)
        form = ProductVersionForm(instance=product_version, data=request.POST)
        if form.is_valid():
            form.instance.product = product
            form.save()
            messages.success(request, "Product Version updated successfully")
        return redirect("admins:product-detail", product_id)


@method_decorator(vendor_or_admin_required, name='dispatch')
class ProductVersionDeleteView(View):

    def get(self, request, product_id, pk):
        product = get_object_or_404(Product, pk=product_id)
        product_version = get_object_or_404(ProductVersion.objects.filter(product=product), pk=pk)
        product_version.delete()
        messages.success(request, "Product Version deleted successfully")
        return redirect("admins:product-detail", product_id)

    def post(self, request, product_id, pk):
        product = get_object_or_404(Product, pk=product_id)
        product_version = get_object_or_404(ProductVersion.objects.filter(product=product), pk=pk)
        product_version.delete()
        messages.success(request, "Product Version deleted successfully")
        return redirect("admins:product-detail", product_id)


@method_decorator(vendor_or_admin_required, name='dispatch')
class ProductImageAddView(View):

    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        form = ProductImageForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.instance.product = product
            form.save()
            messages.success(request, "Product Image added successfully")
        return redirect("admins:product-detail", product_id)


@method_decorator(vendor_or_admin_required, name='dispatch')
class ProductImageDeleteView(View):

    def get(self, request, product_id, pk):
        product = get_object_or_404(Product, pk=product_id)
        product_image = get_object_or_404(ProductImage.objects.filter(product=product), pk=pk)
        product_image.delete()
        messages.success(request, "Product Image deleted successfully")
        return redirect("admins:product-detail", product_id)

    def post(self, request, product_id, pk):
        product = get_object_or_404(Product, pk=product_id)
        product_image = get_object_or_404(ProductImage.objects.filter(product=product), pk=pk)
        product_image.delete()
        messages.success(request, "Product Image deleted successfully")
        return redirect("admins:product-detail", product_id)


@method_decorator(vendor_or_admin_required, name='dispatch')
class ProductOtherPlatformAdd(View):

    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        form = ProductPlatformForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.instance.product = product
            form.save()
            messages.success(request, "Product Image added successfully")
        return redirect("admins:product-detail", product_id)


@method_decorator(vendor_or_admin_required, name='dispatch')
class ProductOtherPlatformDelete(View):

    def get(self, request, product_id, pk):
        product = get_object_or_404(Product, pk=product_id)
        other_platform = get_object_or_404(OtherPlatform, pk=pk, product=product)
        other_platform.delete()
        messages.success(request, "Product Platform deleted successfully")
        return redirect("admins:product-detail", product_id)
    def post(self, request, product_id, pk):
        product = get_object_or_404(Product, pk=product_id)
        other_platform = get_object_or_404(OtherPlatform, pk=pk, product=product)
        other_platform.delete()
        messages.success(request, "Product Platform deleted successfully")
        return redirect("admins:product-detail", product_id)


""" ORDERS """


@method_decorator(vendor_or_admin_required, name='dispatch')
class OrderListView(ListView):
    paginate_by = 25

    def get_queryset(self):
        # Get the current seller's profile
        seller_profile = self.request.user.vendor_profile

        # Filter orders that have order items associated with this seller
        return Order.objects.filter(orderitem__seller=seller_profile).distinct()

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        _filter = OrderFilter(self.request.GET, queryset=self.get_queryset())
        context['filter_form'] = _filter.form

        paginator = Paginator(_filter.qs, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_object = paginator.get_page(page_number)

        context['object_list'] = page_object
        return context



@method_decorator(vendor_or_admin_required, name='dispatch')
class OrderDetailView(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(pk=self.object.pk)
        return context


@method_decorator(vendor_or_admin_required, name='dispatch')
class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('admins:Order-list')


@method_decorator(vendor_or_admin_required, name='dispatch')
class OrderStatusChangeView(View):

    def get(self, request, pk):
        pass


""" BLOG """


@method_decorator(vendor_or_admin_required, name='dispatch')
class PostListView(ListView):
    queryset = Post.objects.all()
    paginate_by = 16

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        _filter = PostFilter(self.request.GET, queryset=Post.objects.filter())
        context['filter_form'] = _filter.form

        paginator = Paginator(_filter.qs, 16)
        page_number = self.request.GET.get('page')
        page_object = paginator.get_page(page_number)

        context['object_list'] = page_object
        return context


@method_decorator(vendor_or_admin_required, name='dispatch')
class PostDetailView(DetailView):
    model = Post


@method_decorator(vendor_or_admin_required, name='dispatch')
class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('admins:post-list')


@method_decorator(vendor_or_admin_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = [
        'thumbnail_image', 'title', 'category', 'read_time', 'content', 'status'
    ]
    success_url = reverse_lazy('admins:post-list')


@method_decorator(vendor_or_admin_required, name='dispatch')
class PostCreateView(CreateView):
    model = Post
    fields = [
        'thumbnail_image', 'title', 'category', 'read_time', 'content', 'status'
    ]
    success_url = reverse_lazy('admins:post-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)





# @method_decorator(admin_protected, name='dispatch')