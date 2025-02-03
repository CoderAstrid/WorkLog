<template>
  <v-container fluid class="pa-4">
    <v-card>
      <!-- Tabs for Work Log & My Account -->
      <v-tabs v-model="tab">
        <v-tab>Work Logs</v-tab>
        <v-tab>My Account</v-tab>
      </v-tabs>
      <v-tabs-items v-model="tab">
        <!-- Work Logs Tab -->
        <v-tab-item>
          <v-row class="align-center mb-2">
            <v-col cols="6">
              <h3 class="ml-3">Work Logs of {{ username }}</h3>
            </v-col>
            <v-col cols="6" class="text-right">
              <v-btn
                color="error"
                :disabled="selectedLogs.length === 0"
                @click="confirmDeleteDialog = true"
              >
                Delete Selected
              </v-btn>
            </v-col>
          </v-row>
          <v-data-table
            v-model="selectedLogs"
            :headers="headers"
            :items="workLogs"
            item-value="id"
            show-select
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
              <v-textarea
                v-model="item.content"
                density="compact"
                variant="outlined"
                hide-details
                auto-grow
                rows="2"
                @change="updateWorkLog(item)"
              ></v-textarea>
            </template>

            <!-- Editable Notes Column -->
            <template v-slot:item.notes="{ item }">
              <v-textarea
                v-model="item.notes"
                density="compact"
                variant="outlined"
                hide-details
                auto-grow
                rows="2"
                @change="updateWorkLog(item)"
              ></v-textarea>
            </template>
          </v-data-table>
          <v-btn color="success" class="mt-4" @click="addPreviousDay">Add Previous Day</v-btn>
          <!-- 🔴 Delete Confirmation Dialog -->
          <v-dialog v-model="confirmDeleteDialog" max-width="400px">
            <v-card>
              <v-card-title class="headline">Confirm Deletion</v-card-title>
              <v-card-text>
                Are you sure you want to delete the selected work logs?
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="grey" text @click="confirmDeleteDialog = false">Cancel</v-btn>
                <v-btn color="red" text @click="deleteSelectedLogs">Delete</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
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
      selectedLogs: [],  // Store selected log IDs
      confirmDeleteDialog: false,  // ✅ Add this line to fix the warning
      lastAddedDate: new Date(),
      tab: 0,      
      headers: [
        { text: "", value: "data-table-select", width: "30px" },  // Checkbox Column
        { text: "Date", value: "date" , width: "120px"},
        { text: "Work Content", value: "content", width: "auto" },
        { text: "Notes", value: "notes", width: "auto" },
      ],
    };
  },
  async mounted() {
    this.fetchProfile();
    this.fetchWorkLogs();    
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
        // Correctly assign the username from API response
        this.username = response.data.username;
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
      const token = localStorage.getItem("token");
      try {
        if (item.id) {
          // If ID exists, update existing log in DB
          await this.$http.put(`worklogs/${item.id}/update/`, item, {
            headers: { Authorization: `Token ${token}` },
          });
        } else {
          // If no ID, this is a new row -> Save it to DB for the first time
          const response = await this.$http.post("worklogs/add/", {
            date: item.date,
            content: item.content,
            notes: item.notes,
          }, {
            headers: { Authorization: `Token ${token}` },
          });
          item.id = response.data.id; // Assign ID after saving to DB
        }
      } catch (error) {
        console.error("Error updating work log:", error);
      }
    },
    async deleteSelectedLogs() {
      this.confirmDeleteDialog = false
      if (!this.selectedLogs.length) return;

      // const confirmed = confirm("Are you sure you want to delete the selected work logs?");
      // if (!confirmed) return;

      try {
        for (const log of this.selectedLogs) {
          if (!log.id) continue;  // ✅ Ensure only valid IDs are processed
          await this.$http.delete(`worklogs/${log.id}/delete/`, {
            headers: { Authorization: `Token ${localStorage.getItem("token")}` },
          });
        }
        
        // Remove deleted logs from UI
        this.workLogs = this.workLogs.filter(log => !this.selectedLogs.includes(log));
        this.selectedLogs = []; // Clear selection
      } catch (error) {
        console.error("Error deleting work logs:", error);
      }
    },
  },
};
</script>
<style scoped>
.v-container {
  min-height: 100vh;
}
</style>
