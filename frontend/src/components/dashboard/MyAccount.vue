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
                    <!-- ✅ New Password (Optional) -->
                    <v-text-field 
                        v-model="newPassword" 
                        label="New Password (Optional)" 
                        type="password" 
                        outlined
                        dense
                        hide-details
                        placeholder="Enter new password"
                        class="mb-4"
                    ></v-text-field>
                    <!-- ✅ Confirm New Password (Only appears if new password is entered) -->
                    <!-- ✅ Confirm Password (Only shows if newPassword is entered) -->
                    <v-text-field
                        v-if="newPassword"
                        v-model="confirmPassword"
                        label="Confirm Password"
                        type="password"
                        outlined
                        dense
                        hide-details
                        placeholder="Re-enter new password"
                        class="mb-4"
                    ></v-text-field>
                    <!-- ✅ Show Validation Message -->
                    <p v-if="passwordMismatch" class="error-message">⚠ Passwords do not match.</p>
                    <!-- ✅ Action Buttons -->
                    <v-btn color="primary" type="submit" :disabled="passwordMismatch">
                        Save Changes
                    </v-btn>
                </v-form>
            </v-card>
        </v-col>
    </v-row>
</v-container>
</template>

<style scoped>
/* ✅ Adjusted Top & Left Margin */
.account-container {
    min-height: 90vh;
    /* Reduced height */
    display: flex;
    align-items: flex-start;
    /* Align closer to the top */
    justify-content: center;
    padding-top: 30px;
    /* Reduced top margin */
}

/* ✅ Account Card */
.account-card {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 10px;
    box-shadow: 0px 3px 10px rgba(0, 0, 0, 0.15);
    padding: 15px;
    /* Compact Padding */
    max-width: 450px;
    /* Adjust width */
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
        isAdmin: Boolean, // Determine if this is the admin's profile
    },
    data() {
        return {
            userProfile: {
                username: "",
                first_name: "",
                last_name: "",
                email: "",
                role: "user", // Default role to "user"
            },
            newPassword: "",       // ✅ Stores new password
            confirmPassword: "",   // ✅ Stores confirmation password
        };
    },
    computed: {
        passwordMismatch() {
            return this.newPassword !== "" && this.newPassword !== this.confirmPassword;
        },
    },
    async mounted() {
        this.fetchProfile();
    },
    methods: {
        async fetchProfile() {
            try {
                const endpoint = this.isAdmin ? "admin/profile/" : "user/profile/";
                const response = await this.$http.get(endpoint, {
                    headers: {
                        Authorization: `Token ${localStorage.getItem("token")}`
                    },
                });

                this.userProfile = {
                    username: response.data.username,
                    first_name: response.data.first_name,
                    last_name: response.data.last_name,
                    email: response.data.email,
                    role: response.data.role, // ✅ Assign the correct role (admin/user)                    
                };
            } catch (error) {
                console.error("Error fetching user profile:", error);
            }
        },
        async updateProfile() {
            if (this.passwordMismatch) {
                alert("Passwords do not match. Please correct and try again.");
                return;
            }

            try {
                const endpoint = this.isAdmin ? "admin/profile/" : "user/profile/";

                const updateData = { ...this.userProfile };
                if (this.newPassword !== "") {
                    updateData.password = this.newPassword; // ✅ Only send password if filled
                }

                await this.$http.put(endpoint, updateData, {
                    headers: { Authorization: `Token ${localStorage.getItem("token")}` },
                });

                alert("Profile updated successfully!");
                this.newPassword = "";
                this.confirmPassword = ""; // ✅ Clear password fields after saving
            } catch (error) {
                console.error("Error updating profile:", error);
            }
        },
    },
};
</script>
