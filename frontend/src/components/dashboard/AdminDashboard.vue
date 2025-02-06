<template>
    <v-container fluid class="pa-4">
      <v-card>
        <v-toolbar flat color="green" dark>
          <v-toolbar-title>Administrator Dashboard</v-toolbar-title>
        </v-toolbar>
  
        <v-tabs v-model="activeTab">
          <v-tab>📋 Work Logs</v-tab>
          <v-tab>👥 Management</v-tab>
          <v-tab>🙍‍♂️ My Account</v-tab>
        </v-tabs>
  
        <v-tabs-items v-model="activeTab">
          <v-tab-item>
            <WorkLogs />
          </v-tab-item>
          <v-tab-item>
            <UserManagement />
          </v-tab-item>
          <v-tab-item>
            <MyAccount />
          </v-tab-item>
        </v-tabs-items>
      </v-card>
    </v-container>
  </template>
  
  <script>
  import WorkLogs from "@/components/dashboard/WorkLogs.vue";
  import UserManagement from "@/components/dashboard/UserManagement.vue";
  import MyAccount from "@/components/dashboard/MyAccount.vue";
  
  export default {
    components: {
      WorkLogs,
      UserManagement,
      MyAccount,
    },
    data() {
      return {
        activeTab: 0,
      };
    },
  };
  </script>
  
  <style scoped>
  </style>
  