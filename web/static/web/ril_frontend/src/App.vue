<script setup>
import LoadingIndicator from '@/components/LoadingIndicator.vue';
</script>

<template>
  <form @submit.prevent="saveArticle" method="post">
    <p>{{ successMessage }}</p>
    <p>{{ errorMessage }}</p>
    <input type="text" class="form-control" id="url" v-model="formData.url">
    <br>
    <LoadingIndicator v-if="isLoading"/>
    <button v-else class="btn btn-primary">Добавить</button>
  </form>
</template>

<script>
import axios from 'axios';
import {API_URL} from "@/consts";
import Cookies from 'js-cookie'

export default {
  name: 'App',
  data() {
    return {
      formData: {url: ''},
      // csrfToken: '',
      isLoading: false,
      successMessage: '',
      errorMessage: ''
    };
  },

  created() {
    this.formData.csrfToken = Cookies.get('csrftoken')
  },

  methods: {
    saveArticle() {
      // this.csrfToken = Cookies.get('csrftoken')
      this.isLoading = true;
      // axios.defaults.xsrfHeaderName = "X-CSRFToken";
      // axios.defaults.xsrfCookieName = "csrftoken";
      this.formData.user = document.querySelector('[id=user]').value
      console.log(this.formData)
      axios.post(
          `${API_URL}/api/save_pdf`, this.formData,
          {
            // headers: {
            //   'X-CSRFToken': `${this.csrfToken}`,
            // },
            // 'withCredentials': true,
          }
      )
          // eslint-disable-next-line no-unused-vars
          .then(response => {
            this.formData.url = ''
            this.successMessage = 'Статья успешно сохранена'
            this.isLoading = false;
          })
          .catch(error => {
            this.isLoading = false;
            this.errorMessage = error.message;
          });
    }
  },
};
</script>
