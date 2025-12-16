import { defineStore } from 'pinia'
import axios from 'axios'

const API_URL = 'http://localhost:8000/api'

export const useArticleStore = defineStore('article', {
  state: () => ({
    articles: [],
    currentArticle: null,
    loading: false,
    error: null,
    pagination: {
      count: 0,
      next: null,
      previous: null
    }
  }),

  actions: {
    async fetchArticles(page = 1) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get(`${API_URL}/articles/?page=${page}`)
        this.articles = response.data.results
        this.pagination = {
          count: response.data.count,
          next: response.data.next,
          previous: response.data.previous
        }
      } catch (error) {
        this.error = 'Помилка при завантаженні статей'
        console.error('Error fetching articles:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchArticle(id) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get(`${API_URL}/articles/${id}/`)
        this.currentArticle = response.data
      } catch (error) {
        this.error = 'Помилка при завантаженні статті'
        console.error('Error fetching article:', error)
      } finally {
        this.loading = false
      }
    },

    async addComment(articleId, commentData) {
      try {
        const response = await axios.post(`${API_URL}/comments/`, {
          article: articleId,
          ...commentData
        })
        // Оновлюємо статтю для отримання нового коментаря
        await this.fetchArticle(articleId)
        return response.data
      } catch (error) {
        this.error = 'Помилка при додаванні коментаря'
        console.error('Error adding comment:', error)
        throw error
      }
    }
  }
})

