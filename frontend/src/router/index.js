import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Публичные страницы
import HomePage from '@/views/public/HomePage.vue'
import BookCatalogPage from '@/views/public/BookCatalogPage.vue'
import BookDetailPublicPage from '@/views/public/BookDetailPublicPage.vue'
import AuthorsPage from '@/views/public/AuthorsPage.vue'
import GenresPage from '@/views/public/GenresPage.vue'
import AboutPage from '@/views/public/AboutPage.vue'

// Страницы авторизации
import RoleSelectPage from '@/views/auth/RoleSelectPage.vue'
import ReaderLoginPage from '@/views/auth/ReaderLoginPage.vue'
import LibrarianLoginPage from '@/views/auth/LibrarianLoginPage.vue'
import AdminLoginPage from '@/views/auth/AdminLoginPage.vue'
import RegisterPage from '@/views/auth/RegisterPage.vue'

// Защищенные страницы
import ProfilePage from '@/views/ProfilePage.vue'
import NotFoundPage from '@/views/NotFoundPage.vue'
import UnauthorizedPage from '@/views/UnauthorizedPage.vue'

// Дашборды
import ReaderDashboard from '@/views/dashboard/ReaderDashboard.vue'
import LibrarianDashboard from '@/views/dashboard/LibrarianDashboard.vue'
import AdminDashboard from '@/views/dashboard/AdminDashboard.vue'

// Книги (защищенные)
import BookListPage from '@/views/books/BookListPage.vue'
import BookDetailPage from '@/views/books/BookDetailPage.vue'
import BookCreatePage from '@/views/books/BookCreatePage.vue'
import BookEditPage from '@/views/books/BookEditPage.vue'

// Копии
import CopyManagementPage from '@/views/copies/CopyManagementPage.vue'

// Выдачи
import ActiveLoansPage from '@/views/loans/ActiveLoansPage.vue'
import OverdueLoansPage from '@/views/loans/OverdueLoansPage.vue'
import LoanHistoryPage from '@/views/loans/LoanHistoryPage.vue'
import LoanCreatePage from '@/views/loans/LoanCreatePage.vue'

// Пользователи
import UserListPage from '@/views/users/UserListPage.vue'
import UserDetailPage from '@/views/users/UserDetailPage.vue'
import UserCreatePage from '@/views/users/UserCreatePage.vue'
import UserEditPage from '@/views/users/UserEditPage.vue'

// Читатели
import MyBooksPage from '@/views/reader/MyBooksPage.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
    meta: { layout: 'public', requiresAuth: false }
  },
  {
    path: '/books',
    name: 'BookCatalog',
    component: BookCatalogPage,
    meta: { layout: 'public', requiresAuth: false }
  },
  {
    path: '/books/:id',
    name: 'BookDetailPublic',
    component: BookDetailPublicPage,
    meta: { layout: 'public', requiresAuth: false }
  },
  {
    path: '/authors',
    name: 'Authors',
    component: AuthorsPage,
    meta: { layout: 'public', requiresAuth: false }
  },
  {
    path: '/genres',
    name: 'Genres',
    component: GenresPage,
    meta: { layout: 'public', requiresAuth: false }
  },
  {
    path: '/about',
    name: 'About',
    component: AboutPage,
    meta: { layout: 'public', requiresAuth: false }
  },
  {
    path: '/login',
    name: 'RoleSelect',
    component: RoleSelectPage,
    meta: { layout: 'auth', requiresAuth: false }
  },
  {
    path: '/login/reader',
    name: 'ReaderLogin',
    component: ReaderLoginPage,
    meta: { layout: 'auth', requiresAuth: false }
  },
  {
    path: '/login/librarian',
    name: 'LibrarianLogin',
    component: LibrarianLoginPage,
    meta: { layout: 'auth', requiresAuth: false }
  },
  {
    path: '/login/admin',
    name: 'AdminLogin',
    component: AdminLoginPage,
    meta: { layout: 'auth', requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterPage,
    meta: { layout: 'auth', requiresAuth: false }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfilePage,
    meta: { layout: 'default', requiresAuth: true }
  },
  {
    path: '/reader/dashboard',
    name: 'ReaderDashboard',
    component: ReaderDashboard,
    meta: { layout: 'default', requiresAuth: true, roles: ['reader'] }
  },
  {
    path: '/librarian/dashboard',
    name: 'LibrarianDashboard',
    component: LibrarianDashboard,
    meta: { layout: 'default', requiresAuth: true, roles: ['librarian', 'admin'] }
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { layout: 'default', requiresAuth: true, roles: ['admin'] }
  },
  {
    path: '/admin/books',
    name: 'BookList',
    component: BookListPage,
    meta: { layout: 'default', requiresAuth: true, roles: ['admin', 'librarian'] }
  },
  {
    path: '/admin/books/create',
    name: 'BookCreate',
    component: BookCreatePage,
    meta: { layout: 'default', requiresAuth: true, roles: ['admin', 'librarian'] }
  },
  {
    path: '/admin/books/:id/edit',
    name: 'BookEdit',
    component: BookEditPage,
    meta: { layout: 'default', requiresAuth: true, roles: ['admin', 'librarian'] }
  },
  {
    path: '/admin/books/:id',
    name: 'BookDetail',
    component: BookDetailPage,
    meta: { layout: 'default', requiresAuth: true, roles: ['admin', 'librarian'] }
  },
  {
    path: '/admin/copies',
    name: 'CopyManagement',
    component: CopyManagementPage,
    meta: { layout: 'default', requiresAuth: true, roles: ['admin', 'librarian'] }
  },
  {
    path: '/admin/loans',
    name: 'ActiveLoans',
    component: ActiveLoansPage,
    meta: { layout: 'default', requiresAuth: true, roles: ['admin', 'librarian'] }
  },
  {
    path: '/admin/loans/overdue',
    name: 'OverdueLoans',
    component: OverdueLoansPage,
    meta: { layout: 'default', requiresAuth: true, roles: ['admin', 'librarian'] }
  },
  {
    path: '/admin/loans/history',
    name: 'LoanHistory',
    component: LoanHistoryPage,
    meta: { layout: 'default', requiresAuth: true, roles: ['admin', 'librarian'] }
  },
  {
    path: '/admin/loans/create',
    name: 'LoanCreate',
    component: LoanCreatePage,
    meta: { layout: 'default', requiresAuth: true, roles: ['admin', 'librarian'] }
  },
  {
    path: '/admin/users',
    name: 'UserList',
    component: UserListPage,
    meta: { layout: 'default', requiresAuth: true, roles: ['admin'] }
  },
  {
    path: '/admin/users/create',
    name: 'UserCreate',
    component: UserCreatePage,
    meta: { layout: 'default', requiresAuth: true, roles: ['admin'] }
  },
  {
    path: '/admin/users/:id',
    name: 'UserDetail',
    component: UserDetailPage,
    meta: { layout: 'default', requiresAuth: true, roles: ['admin'] }
  },
  {
    path: '/admin/users/:id/edit',
    name: 'UserEdit',
    component: UserEditPage,
    meta: { layout: 'default', requiresAuth: true, roles: ['admin'] }
  },
  {
    path: '/unauthorized',
    name: 'Unauthorized',
    component: UnauthorizedPage,
    meta: { layout: 'empty', requiresAuth: false }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFoundPage,
    meta: { layout: 'empty', requiresAuth: false }
  },
  {
  path: '/reader/books',
  name: 'MyBooks',
  component: MyBooksPage,
  meta: { layout: 'default', requiresAuth: true, roles: ['reader'] }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// Навигационный гард
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // Ждем инициализации auth store
  if (!authStore.initialized) {
    await authStore.initAuth()
  }

  const requiresAuth = to.meta.requiresAuth
  const requiredRoles = to.meta.roles || []

  // Публичные маршруты (не требуют авторизации)
  if (!requiresAuth) {
    // Если пользователь авторизован и пытается зайти на страницы логина,
    // перенаправляем его в соответствующий дашборд
    if (authStore.isAuthenticated && to.path.startsWith('/login')) {
      const dashboardRoute = authStore.getDashboardRoute()
      return next(dashboardRoute)
    }
    return next()
  }

  // Маршруты, требующие авторизации
  if (!authStore.isAuthenticated) {
    return next('/login')
  }

  // Проверка ролей
  if (requiredRoles.length > 0) {
    const hasRequiredRole = requiredRoles.some(role => authStore.hasRole(role))
    if (!hasRequiredRole) {
      return next('/unauthorized')
    }
  }

  next()
})

export default router