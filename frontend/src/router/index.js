import { createRouter, createWebHistory } from 'vue-router'
import ArticleList from './views/ArticleList.vue'
import ArticleDetail from './views/ArticleDetail.vue'

const routes = [
  {
    path: '/',
    redirect: '/articles'
  },
  {
    path: '/articles',
    name: 'ArticleList',
    component: ArticleList
  },
  {
    path: '/articles/:id',
    name: 'ArticleDetail',
    component: ArticleDetail
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

