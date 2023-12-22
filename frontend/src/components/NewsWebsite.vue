<template>
  <div class="container">
    <header>
      <div class="logo">
        <img :src="background" alt="News Logo">
      </div>
    </header>
    <main>
      <table></table>
      <label for="datepicker">Select a Date:</label>
      <flat-pickr v-model="selectedDate"></flat-pickr>
      <button @click="submitDate">Submit</button>
      <section class="articles" v-for="(data, index) in news" :key="index">
        <article v-for="(article, sindex) in data" :key="sindex">
          <h1>{{ article.title }}</h1>
          <img :src=article.image_url alt="" width="1" height="1">
          <p>{{ formatDate(article.publisher_date) }}</p>
          <a :href=article.news_url>News Url</a>
        </article>
      </section>
      <!-- <article>
          <h2>Article Title</h2>
          <img :src="background" alt="Article Image">
          <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed elementum enim eget quam vulputate, id finibus
            velit aliquam. Donec nec enim a mi aliquam faucibus. Donec sed metus sed enim semper posuere.</p>
          <a href="#">Read More</a>
        </article>
        <article>
          <h2>Article Title</h2>
          <img :src="background" alt="Article Image">
          <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec at quam sed urna vehicula semper. Sed sit amet
            lectus eget ipsum faucibus semper vel et dui.</p>
          <a href="#">Read More</a>
        </article> -->
    </main>
    <footer>
      <p>&copy; 2023 News Website</p>
    </footer>
  </div>
</template>

<script>
import FlatPickr from "vue-flatpickr-component";
import "flatpickr/dist/flatpickr.css";
export default {
  name: 'NewsWebsite',
  components: {
    FlatPickr
  },
  data() {
    return {
      message: '',
      headlines: [],
      connection: null,
      columns: 3,
      selectedDate:''
    };
  },
  created: function () {
    console.log("Starting connection to WebSocket Server", process.env.VUE_APP_WEBSOCKET);
    this.connection = new WebSocket(process.env.VUE_APP_WEBSOCKET);
    this.connection.onopen = () => this.connection.send('{"all_headlines":true}')
  },
  mounted() {
    this.connection.onmessage = (e) => {
      var data = JSON.parse(e.data)
      if (data["success"] == true) {
        console.log("data", data)
        this.headlines.push(data["messege"])
      }
      else {
        this.headlines = []
        this.message = data["messege"]
      }
    };
  },
  computed: {
    background() {
      return process.env.VUE_APP_BASE_URL + "images/news.jpg"
      // return ("/images/news.jpg")
    },
    news() {
      const groups = [];
      for (let i = 0; i < this.headlines.length; i += 3) {
        groups.push(this.headlines.slice(i, i + 3));
      }
      return groups;
    }
  },
  methods: {
    formatDate(timestampString) {
      const date = new Date(timestampString);
      const formattedDate = date.toDateString();
      return formattedDate;
    },
    submitDate() {
      console.log("date", this.selectedDate)
      this.message = '{"date": "'+this.selectedDate+'"}'
      this.connection = new WebSocket(process.env.VUE_APP_WEBSOCKET);
      this.connection.onopen = () => this.connection.send(this.message)
      this.headlines = []
      this.connection.onmessage = (e) => {
        var data = JSON.parse(e.data)
        if (data["success"] == true) {
          console.log("data", data)
          this.headlines.push(data["messege"])
        }
        else {
        this.message = data["messege"]
      }
    };
    }
  },
}
</script>

<style scoped>
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  font-family: sans-serif;
}

header {
  background-color: #fff;
  padding: 20px;
}

.logo {
  float: left;
}

.logo img {
  height: 50px;
}

nav {
  float: right;
}

nav ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

nav li {
  display: inline-block;
  margin-right: 20px;
}

nav a {
  text-decoration: none;
  color: #000;
  font-weight: bold;
}

main {
  padding: 20px;
}

.articles {
  display: flex;
  flex-wrap: wrap;
  /* justify-content: space-around; */
}

article {
  width: 30%;
  margin: 1%;
}

article h2 {
  font-size: 24px;
  margin-bottom: 10px;
}

article img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  margin-bottom: 10px;
}

article p {
  font-size: 16px;
  line-height: 1.5;
}

article a {
  display: block;
  background-color: #007bff;
  color: #fff;
  padding: 10px 20px;
  text-decoration: none;
  margin-top: 10px;
}

footer {
  background-color: #fff;
  padding: 20px;
  text-align: center;
}

button {
  background-color: #007bff;
  color: #fff;
  /* padding: 10px 20px; */
  text-decoration: none;
  margin-top: 10px;
}
</style>

