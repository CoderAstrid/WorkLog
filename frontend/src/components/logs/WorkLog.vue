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
          <h3 class="ml-3">Work Logs of {{ username }}</h3>          
          <v-data-table
            v-model="workLogs"
            :headers="headers"
            :items="workLogs"
            item-value="id"
            class="elevation-1 mt-4"
            dense
          >
            <!-- Editable Date Column -->
            <template v-slot:item.date="{ item }">
              <v-menu
                v-model="item.datePicker"
                :close-on-content-click="false"
                transition="scale-transition"
                offset-y
                min-width="auto"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    v-model="item.date"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                    dense
                    variant="outlined"
                    hide-details
                  ></v-text-field>
                </template>
                <v-date-picker
                  v-model="item.date"
                  :max="today"
                  :allowed-dates="allowedDates"
                  @input="updateWorkLog(item)"
                ></v-date-picker>
              </v-menu>
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
        { text: "Date", value: "date" , width: "120px"},
        { text: "Work Content", value: "content", width: "auto" },
        { text: "Notes", value: "notes", width: "auto" },
      ],
      today: new Date().toISOString().split("T")[0],
    };
  },
  async mounted() {
    this.fetchProfile();
    this.fetchWorkLogs();    
  },
  methods: {
    allowedDates(date) {
      return (
        date <= this.today && // Prevent future dates
        !this.workLogs.some((log) => log.date === date) // Prevent duplicate dates
      );
    },
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
      const today = new Date();
      let previousDate = new Date(this.lastAddedDate);
      
      do {
        previousDate.setDate(previousDate.getDate() - 1);
      } while (
        this.workLogs.some(log => log.date === previousDate.toISOString().split("T")[0]) || // Rule 2: Avoid duplicate dates
        previousDate >= today // Rule 1: Must be earlier than today
      );

      this.lastAddedDate = previousDate;

      this.workLogs.push({
        id: null, // No ID since it's not in DB yet
        date: previousDate.toISOString().split("T")[0],
        content: "",
        notes: "",
      });
    },
    async updateWorkLog(item) {
      const today = new Date().toISOString().split("T")[0]; // Get today's date
      const newDate = item.date;

      // Rule 1: The new date cannot be after today
      if (newDate > today) {
        alert("The date cannot be in the future.");
        item.date = today; // Reset to today's date
        return;
      }
      
      // Rule 2: The new date must not overlap with any of the existing recorded dates
      if (this.workLogs.some(log => log.id !== item.id && log.date === newDate)) {
        alert("A record with this date already exists. Please choose a different date.");
        return;
      }

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
  },
};
</script>
<style scoped>
.v-container {
  min-height: 100vh;
}
</style>
