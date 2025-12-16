<template>
  <div class="container">
    <h1>Статті блогу</h1>

    <div v-if="store.loading" class="loading">
      Завантаження...
    </div>

    <div v-else-if="store.error" class="error">
      {{ store.error }}
    </div>

    <div v-else>
      <div v-if="store.articles.length === 0" class="no-articles">
        Статті не знайдено
      </div>

      <div v-else class="articles-grid">
        <div v-for="article in store.articles" :key="article.id" class="article-card card">
          <div class="article-header">
            <h2>
              <router-link :to="`/articles/${article.id}`" class="article-title">
                {{ article.title }}
              </router-link>
            </h2>
            <span class="article-category">{{ article.category_name }}</span>
          </div>

          <div class="article-meta">
            <span class="author">Автор: {{ article.author || article.user_username || 'Анонім' }}</span>
            <span class="date">{{ formatDate(article.publication_date) }}</span>
          </div>

          <p class="article-excerpt">{{ getExcerpt(article.text) }}</p>

          <div class="article-footer">
            <router-link :to="`/articles/${article.id}`" class="btn btn-primary">
              Читати далі
            </router-link>
            <span class="comments-count">
              💬 {{ article.comments_count || 0 }} коментарів
            </span>
          </div>
        </div>
      </div>

      <div v-if="store.pagination.count > 10" class="pagination">
        <button
          @click="changePage(currentPage - 1)"
          :disabled="!store.pagination.previous"
          class="btn"
        >
          Попередня
        </button>
        <span class="page-info">Сторінка {{ currentPage }}</span>
        <button
          @click="changePage(currentPage + 1)"
          :disabled="!store.pagination.next"
          class="btn"
        >
          Наступна
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useArticleStore } from '../stores/article'

const store = useArticleStore()
const currentPage = ref(1)

onMounted(() => {
  store.fetchArticles(currentPage.value)
})

const changePage = (page) => {
  currentPage.value = page
  store.fetchArticles(page)
  window.scrollTo(0, 0)
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('uk-UA', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const getExcerpt = (text) => {
  const maxLength = 200
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}
</script>

<style scoped>
h1 {
  margin-bottom: 2rem;
  color: #2c3e50;
}

.articles-grid {
  display: grid;
  gap: 1.5rem;
}

.article-card {
  transition: transform 0.2s;
}

.article-card:hover {
  transform: translateY(-4px);
}

.article-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.article-title {
  color: #2c3e50;
  text-decoration: none;
  font-size: 1.5rem;
  margin: 0;
}

.article-title:hover {
  color: #3498db;
}

.article-category {
  background-color: #3498db;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.875rem;
  white-space: nowrap;
}

.article-meta {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1rem;
  color: #666;
  font-size: 0.875rem;
}

.article-excerpt {
  color: #555;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.comments-count {
  color: #666;
  font-size: 0.875rem;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
  padding: 1rem;
}

.page-info {
  padding: 0 1rem;
  font-weight: 500;
}

.pagination .btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.no-articles {
  text-align: center;
  padding: 3rem;
  color: #666;
  font-size: 1.2rem;
}
</style>

