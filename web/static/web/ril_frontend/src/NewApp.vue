<template>
  <form method="post" @submit.prevent="saveArticle">
    <input type="text">
    <button>Добавить</button>
  </form>
</template>

<script>
import axios from "axios";
import {API_URL} from "@/consts";

export default {
  name: "NewApp",

  data() {
    return {
      url: '',
      csrfToken: '',
      message: '',
    }
  },

  methods: {
    saveArticle() {
      axios.defaults.xsrfHeaderName = "X-CSRFToken";
      axios.defaults.xsrfCookieName = "csrftoken";

      axios.post(
          `${API_URL}/files/add/vue`,
          {url: this.url},
          {'withCredentials': true}
      )
          .then(response => {
            console.log(response.status)
          })
          .catch(error => {
            console.log(error.message)
          })
    }
  }
}
</script>

