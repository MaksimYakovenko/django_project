<template>
  <div class="container">
    <div v-if="store.loading" class="loading">
      Завантаження...
    </div>

    <div v-else-if="store.error" class="error">
      {{ store.error }}
    </div>

    <div v-else-if="store.currentArticle" class="article-detail">
      <div class="article-header">
        <router-link to="/articles" class="back-link">← Назад до списку</router-link>
        <h1>{{ store.currentArticle.title }}</h1>

        <div class="article-meta">
          <span class="category">{{ store.currentArticle.category_name }}</span>
          <span class="author">Автор: {{ store.currentArticle.author || store.currentArticle.user_username || 'Анонім' }}</span>
          <span class="date">{{ formatDate(store.currentArticle.publication_date) }}</span>
        </div>

        <div v-if="store.currentArticle.tags && store.currentArticle.tags.length" class="tags">
          <span v-for="tag in store.currentArticle.tags" :key="tag.id" class="tag">
            #{{ tag.title }}
          </span>
        </div>
      </div>

      <div v-if="store.currentArticle.image" class="article-image">
        <img :src="store.currentArticle.image" :alt="store.currentArticle.title">
      </div>

      <div class="article-content card">
        <p>{{ store.currentArticle.text }}</p>
      </div>

      <div class="comments-section">
        <h2>Коментарі ({{ store.currentArticle.comments ? store.currentArticle.comments.length : 0 }})</h2>

        <div class="comment-form card">
          <h3>Додати коментар</h3>
          <form @submit.prevent="submitComment">
            <div class="form-group">
              <label for="author">Ваше ім'я:</label>
              <input
                type="text"
                id="author"
                v-model="commentForm.author"
                required
                class="form-control"
              >
            </div>
            <div class="form-group">
              <label for="text">Коментар:</label>
              <textarea
                id="text"
                v-model="commentForm.text"
                rows="4"
                required
                class="form-control"
              ></textarea>
            </div>
            <button type="submit" class="btn btn-primary" :disabled="submitting">
              {{ submitting ? 'Надсилання...' : 'Додати коментар' }}
            </button>
          </form>
        </div>

        <div v-if="store.currentArticle.comments && store.currentArticle.comments.length" class="comments-list">
          <div v-for="comment in store.currentArticle.comments" :key="comment.id" class="comment card">
            <div class="comment-header">
              <strong>{{ comment.author || comment.user_username || 'Анонім' }}</strong>
              <span class="comment-date">{{ formatDate(comment.publication_date) }}</span>
            </div>
            <p class="comment-text">{{ comment.text }}</p>
          </div>
        </div>

        <div v-else class="no-comments">
          Коментарів поки немає. Будьте першим!
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useArticleStore } from '../stores/article'

const route = useRoute()
const store = useArticleStore()

const commentForm = ref({
  author: '',
  text: ''
})

const submitting = ref(false)

onMounted(() => {
  const articleId = route.params.id
  store.fetchArticle(articleId)
})

const submitComment = async () => {
  if (!commentForm.value.author.trim() || !commentForm.value.text.trim()) {
    return
  }

  submitting.value = true
  try {
    await store.addComment(route.params.id, {
      author: commentForm.value.author,
      text: commentForm.value.text
    })

    // Очищаємо форму
    commentForm.value.author = ''
    commentForm.value.text = ''
  } catch (error) {
    alert('Помилка при додаванні коментаря')
  } finally {
    submitting.value = false
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('uk-UA', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<style scoped>
.back-link {
  color: #3498db;
  text-decoration: none;
  margin-bottom: 1rem;
  display: inline-block;
}

.back-link:hover {
  text-decoration: underline;
}

h1 {
  color: #2c3e50;
  margin: 1rem 0;
}

.article-meta {
  display: flex;
  gap: 1.5rem;
  margin: 1rem 0;
  color: #666;
  flex-wrap: wrap;
}

.category {
  background-color: #3498db;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.875rem;
}

.tags {
  display: flex;
  gap: 0.5rem;
  margin: 1rem 0;
  flex-wrap: wrap;
}

.tag {
  background-color: #ecf0f1;
  color: #2c3e50;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.875rem;
}

.article-image {
  margin: 2rem 0;
}

.article-image img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
}

.article-content {
  margin: 2rem 0;
  line-height: 1.8;
  font-size: 1.1rem;
}

.comments-section {
  margin-top: 3rem;
}

.comments-section h2 {
  margin-bottom: 1.5rem;
  color: #2c3e50;
}

.comment-form {
  margin-bottom: 2rem;
}

.comment-form h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.form-control {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  font-family: inherit;
}

.form-control:focus {
  outline: none;
  border-color: #3498db;
}

textarea.form-control {
  resize: vertical;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.comment {
  background-color: #f8f9fa;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #dee2e6;
}

.comment-date {
  color: #666;
  font-size: 0.875rem;
}

.comment-text {
  color: #333;
  line-height: 1.6;
}

.no-comments {
  text-align: center;
  padding: 2rem;
  color: #666;
  font-style: italic;
}
</style>

