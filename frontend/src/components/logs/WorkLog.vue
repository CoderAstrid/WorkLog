<template>
  <v-container class="green-background fill-height d-flex align-center justify-center">
    <v-card class="pa-5" max-width="900">
      <v-tabs v-model="tab">
        <v-tab>Work Logs</v-tab>
        <v-tab>My Account</v-tab>
      </v-tabs>
      <v-tabs-items v-model="tab">
        <!-- Work Logs Tab -->
        <v-tab-item>
          <v-data-table
            :headers="headers"
            :items="workLogs"
            item-value="id"
            class="elevation-1 mt-4"
            dense
          >
            <!-- Editable Date Column -->
            <template v-slot:item.date="{ item }">
              <v-text-field
                v-model="item.date"
                type="date"
                density="compact"
                variant="outlined"
                hide-details
                @change="updateWorkLog(item)"
              ></v-text-field>
            </template>

            <!-- Editable Work Content Column -->
            <template v-slot:item.content="{ item }">
              <v-text-field
                v-model="item.content"
                density="compact"
                variant="outlined"
                hide-details
                @change="updateWorkLog(item)"
              ></v-text-field>
            </template>

            <!-- Editable Notes Column -->
            <template v-slot:item.notes="{ item }">
              <v-text-field
                v-model="item.notes"
                density="compact"
                variant="outlined"
                hide-details
                @change="updateWorkLog(item)"
              ></v-text-field>
            </template>
          </v-data-table>
          <v-btn color="success" class="mt-4" @click="addPreviousDay">Add Previous Day</v-btn>
        </v-tab-item>

        <!-- My Account Tab -->
        <v-tab-item>
          <MyAccount :isAdmin="false" />
        </v-tab-item>
      </v-tabs-items>
    </v-card>
  </v-container>
</template>

<script>
import MyAccount from "@/components/dashboard/MyAccount.vue";  // Import the reusable component

export default {
  components: {
    MyAccount,
  },
  data() {
    return {
      username: localStorage.getItem("username") || "User",
      workLogs: [],
      lastAddedDate: new Date(),
      tab: 0,      
      headers: [
        { text: "Date", value: "date" },
        { text: "Work Content", value: "content" },
        { text: "Notes", value: "notes" },
      ],
    };
  },
  async mounted() {
    this.fetchWorkLogs();
    this.fetchProfile();
  },
  methods: {
    async fetchWorkLogs() {
      try {
        const response = await this.$http.get("worklogs/", {
          headers: { Authorization: `Token ${localStorage.getItem("token")}` },
        });
        this.workLogs = response.data;
      } catch (error) {
        console.error("Error fetching work logs:", error);
      }
    },
    async fetchProfile() {
      try {
        const response = await this.$http.get("user/profile/", {
          headers: { Authorization: `Token ${localStorage.getItem("token")}` },
        });
        // Store correct user data
        this.userProfile = {
          username: response.data.username,
          email: response.data.email,
          password: "", // Leave blank to avoid accidental password overwrite
        };
        console.log(response);
      } catch (error) {
        console.error("Error fetching user profile:", error);
      }
    },
    async updateProfile() {
      try {
        await this.$http.put("user/profile/", this.userProfile, {
          headers: { Authorization: `Token ${localStorage.getItem("token")}` },
        });
        alert("Profile updated successfully!");
      } catch (error) {
        console.error("Error updating profile:", error);
      }
    },
    async resetPassword() {
      try {
        await this.$http.post("user/reset-password/", {
          email: this.userProfile.email,
        });
        alert("Password reset link sent to email!");
      } catch (error) {
        console.error("Error sending password reset:", error);
      }
    },
    addPreviousDay() {
      // Generate a new previous date (without saving to DB)
      const previousDate = new Date(this.lastAddedDate);
      previousDate.setDate(previousDate.getDate() - 1);
      this.lastAddedDate = previousDate;

      // Add a blank log entry ONLY to the displayed table
      this.workLogs.push({
        id: null, // No ID since it's not in DB yet
        date: previousDate.toISOString().split("T")[0],
        content: "",
        notes: "",
      });
    },
    async updateWorkLog(item) {
      try {
        if (item.id) {
          // If ID exists, update existing log in DB
          await this.$http.put(`worklogs/${item.id}/update/`, item, {
            headers: { Authorization: `Token ${localStorage.getItem("token")}` },
          });
        } else {
          // If no ID, this is a new row -> Save it to DB for the first time
          const response = await this.$http.post("worklogs/add/", item, {
            headers: { Authorization: `Token ${localStorage.getItem("token")}` },
          });
          item.id = response.data.id; // Assign ID after DB save
        }
      } catch (error) {
        console.error("Error updating work log:", error);
      }
    },
    async deleteWorkLog(item) {
      try {
        if (item.id) {
          // Only delete from DB if it has an ID
          await this.$http.delete(`worklogs/${item.id}/delete/`, {
            headers: { Authorization: `Token ${localStorage.getItem("token")}` },
          });
          this.workLogs = this.workLogs.filter((log) => log.id !== item.id);
        } else {
          // If no ID, just remove it from frontend display
          this.workLogs = this.workLogs.filter((log) => log !== item);
        }
      } catch (error) {
        console.error("Error deleting work log:", error);
      }
    },
  },
};
</script>

<style scoped>
.green-background {
  background-color: #4CAF50;
  padding: 20px;
  height: 100vh;
}
</style>
