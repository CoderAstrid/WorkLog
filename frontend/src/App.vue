<template>
  <v-app>
    <!-- Navigation Bar -->
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Company Work Log</v-toolbar-title>
      <v-spacer></v-spacer>

      <template v-if="isLoggedIn">
        <!-- <template v-if="isAdmin">
          <v-btn to="/admin">Admin Panel</v-btn>
          <v-btn to="/worklog">Work Log</v-btn>
          <v-btn @click="logout">Logout</v-btn>
        </template> 
        <template v-else>
          <v-btn @click="logout">Logout</v-btn>
        </template>
        -->
        <v-btn @click="logout">Logout</v-btn>
      </template>      
    </v-app-bar>

    <!-- Main Content -->
    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: "App",
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem("token");
    },
    isAdmin() {
      return localStorage.getItem("role") === "admin";
    },
  },
  methods: {
    logout() {
      localStorage.removeItem("token");
      localStorage.removeItem("role");
      this.$router.push("/login");
    },
  },
};
</script>

<style scoped>
</style>
