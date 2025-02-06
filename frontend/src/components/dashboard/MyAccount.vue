<template>
  <v-container class="account-container">
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6">
        <v-card class="pa-5 account-card">
          <v-card-title class="text-h5 mb-3 text-center">
            {{ isAdmin ? "🙍‍♂️ Admin Profile" : "🙍‍♂️ My Account" }}
          </v-card-title>
          
          <v-form ref="form" @submit.prevent="updateProfile">
            <!-- ✅ User ID (Read-Only) -->
            <v-text-field v-model="userProfile.username" label="User ID" required readonly outlined></v-text-field>

            <v-row>
              <v-col cols="6">
                <v-text-field v-model="userProfile.first_name" label="First Name" required outlined></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field v-model="userProfile.last_name" label="Last Name" required outlined></v-text-field>
              </v-col>
            </v-row>

            <v-text-field v-model="userProfile.email" label="Email" required outlined></v-text-field>

            <!-- ✅ Display Role as a Badge Instead of Checkbox -->
            <v-alert dense :type="userProfile.role === 'admin' ? 'success' : 'info'" class="role-badge">
              {{ userProfile.role === 'admin' ? "✔ Admin" : "✖ User" }}
            </v-alert>

            <!-- ✅ Password Change Field -->
            <v-text-field
              v-model="userProfile.password"
              label="New Password"
              type="password"
              outlined
              hint="Leave empty to keep current password"
              persistent-hint
            ></v-text-field>

            <!-- ✅ Action Buttons -->
            <v-row>
              <v-col>
                <v-btn color="primary" type="submit" block large>Save Changes</v-btn>
              </v-col>
              <v-col>
                <v-btn color="error" block large @click="resetPassword">Reset Password</v-btn>
              </v-col>
            </v-row>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
/* ✅ Adjusted Top & Left Margin */
.account-container {
  min-height: 90vh; /* Reduced height */
  display: flex;
  align-items: flex-start; /* Align closer to the top */
  justify-content: center;
  padding-top: 30px; /* Reduced top margin */
}

/* ✅ Account Card */
.account-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 10px;
  box-shadow: 0px 3px 10px rgba(0, 0, 0, 0.15);
  padding: 15px; /* Compact Padding */
  max-width: 450px; /* Adjust width */
}

/* ✅ Role Badge */
.role-badge {
  text-align: left;
  font-weight: bold;
  margin-bottom: 12px;
}

/* ✅ Buttons */
.v-btn {
  font-weight: bold;
  letter-spacing: 0.5px;
}

/* ✅ Reduce Input Heights for Compact Design */
.v-text-field {
  margin-bottom: 8px;
}
</style>



<script>
export default {
  props: {
    isAdmin: Boolean,  // Determine if this is the admin's profile
  },
  data() {
    return {
      userProfile: {
        username: "",
        first_name: "",
        last_name: "",
        email: "",
        password: "",
        role: "user",  // Default role to "user"
      },
    };
  },
  async mounted() {
    this.fetchProfile();
  },
  methods: {
    async fetchProfile() {
      try {
        const endpoint = this.isAdmin ? "admin/profile/" : "user/profile/";
        const response = await this.$http.get(endpoint, {
          headers: { Authorization: `Token ${localStorage.getItem("token")}` },
        });

        this.userProfile = {
          username: response.data.username,
          first_name: response.data.first_name,
          last_name: response.data.last_name,
          email: response.data.email,
          role: response.data.role, // ✅ Assign the correct role (admin/user)
          password: "", // Leave blank to prevent overwriting
        };
      } catch (error) {
        console.error("Error fetching user profile:", error);
      }
    },
    async updateProfile() {
      try {
        const endpoint = this.isAdmin ? "admin/profile/" : "user/profile/";
        await this.$http.put(endpoint, this.userProfile, {
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
  },
};
</script>
