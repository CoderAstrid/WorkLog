<template>
  <v-container fluid>
    <v-card class="pa-4 elevation-2">
      <!-- ✅ Title & Action Buttons -->
      <v-card-title class="d-flex flex-column flex-md-row align-md-center justify-space-between">
        <h3 class="text-h5 font-weight-bold">📋 All Work Logs</h3>
        <div class="actions mt-2 mt-md-0">
          <v-btn
            color="error"
            class="mr-2"
            :disabled="selectedLogs.length === 0"
            @click="confirmDeleteDialog = true"
          >
            <v-icon left>mdi-delete</v-icon> Delete Selected
          </v-btn>
          <v-btn
            color="success"
            :disabled="selectedLogs.length === 0"
            @click="exportWorkLogs"
          >
            <v-icon left>mdi-download</v-icon> Export to Excel
          </v-btn>
        </div>
      </v-card-title>


      <!-- ✅ Filters Section -->
      <v-card-subtitle>
        <v-row dense class="pa-2">
          <v-col cols="5">
            <v-text-field
              v-model="filterUsername"
              label="🔎 Search by Username"
              prepend-icon="mdi-account-search"
              dense
              clearable
              outlined
              hide-details
              @input="applyFilters"
            ></v-text-field>
          </v-col>
          <v-col cols="3">
            <v-menu
              v-model="startDatePicker"
              :close-on-content-click="false"
              transition="scale-transition"
              min-width="auto"
            >
              <template v-slot:activator="{ on }">
                <v-text-field
                  v-model="startDate"
                  label="📅 Start Date"
                  prepend-icon="mdi-calendar"
                  dense
                  readonly
                  outlined
                  hide-details
                  v-on="on"
                  clearable
                  @click:clear="startDate = ''; applyFilters()"
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="startDate"
                @input="applyFilters"
                @change="startDatePicker = false"
              ></v-date-picker>
            </v-menu>
          </v-col>

          <v-col cols="3">
            <v-menu
              v-model="endDatePicker"
              :close-on-content-click="false"
              transition="scale-transition"
              min-width="auto"
            >
              <template v-slot:activator="{ on }">
                <v-text-field
                  v-model="endDate"
                  label="📅 End Date"
                  prepend-icon="mdi-calendar"
                  dense
                  readonly
                  outlined
                  hide-details
                  v-on="on"
                  clearable
                  @click:clear="endDate = ''; applyFilters()"
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="endDate"
                @input="applyFilters"
                @change="endDatePicker = false"
              ></v-date-picker>
            </v-menu>
          </v-col>

          <v-col cols="1">
            <v-btn color="primary" block @click="fetchWorkLogs">
              <v-icon left>mdi-refresh</v-icon> Reset
            </v-btn>
          </v-col>
        </v-row>
      </v-card-subtitle>

      <!-- ✅ Work Logs Table -->
      <v-data-table
        v-model="selectedLogs"
        :headers="headers"
        :items="filteredWorkLogs"
        item-value="id"
        class="elevation-2 mt-4"
        show-select
        dense
      >
        <template v-slot:item.full_name="{ item }">
          <span>{{ item.first_name }} {{ item.last_name }}</span>
        </template>

        <template v-slot:item.content="{ item }">
          <pre class="multiline-text">{{ item.content }}</pre>
        </template>

        <template v-slot:item.notes="{ item }">
          <pre class="multiline-text">{{ item.notes }}</pre>
        </template>
      </v-data-table>
    </v-card>

    <!-- 🔴 Delete Confirmation Dialog -->
    <v-dialog v-model="confirmDeleteDialog" max-width="400px">
      <v-card class="elevation-3">
        <v-card-title class="text-h6 font-weight-bold red--text">
          <v-icon left color="red">mdi-alert-circle</v-icon> Confirm Deletion
        </v-card-title>
        <v-card-text class="red--text font-weight-bold">
          ⚠️ This action cannot be undone!
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey darken-1" text @click="confirmDeleteDialog = false">Cancel</v-btn>
          <v-btn color="red darken-2" text @click="deleteSelectedLogs">
            <v-icon left>mdi-delete</v-icon> Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<style scoped>
/* ✅ Makes multi-line text wrap properly */
.multiline-text {
  white-space: pre-wrap;
  word-wrap: break-word;
  max-width: 100%;
  font-size: 14px;
  padding: 5px;
}

/* ✅ Title & Button Styling */
.v-card-title {
  font-weight: bold;
  font-size: 20px;
}

/* ✅ Adds Spacing for Cleaner UI */
.v-card-subtitle {
  background: #f9f9f9;
  padding: 12px;
  border-radius: 5px;
}

/* ✅ Makes filters look more structured */
.v-text-field {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 5px;
}

/* ✅ Improves table readability */
.v-data-table {
  border-radius: 8px;
  border: 1px solid #ddd;
  background: #fff;
}

/* ✅ Improve row visibility */
.v-data-table tbody tr:nth-child(even) {
  background-color: #f8f9fa;
}

/* ✅ Confirmation Dialog */
.v-dialog {
  border-radius: 8px;
}

/* ✅ Buttons */
.v-btn {
  text-transform: none;
  font-weight: bold;
  letter-spacing: 0.5px;
}

/* ✅ Center delete dialog text */
.v-card-text {
  text-align: center;
}
</style>

  
<script>
  /* eslint-disable no-unused-vars */
  export default {
    data() {
      return {
        selectedLogs: [],  // Store selected log IDs
        workLogs: [],
        filteredWorkLogs: [], // Filtered work logs
        filterUsername: "",
        startDate: "",
        endDate: "",
        startDatePicker: false,
        endDatePicker: false,
        confirmDeleteDialog: false,  // ✅ Add this property
        headers: [
          { text: "", value: "data-table-select", width: "30px" },  // Checkbox Column
          { text: "Date", value: "date", width: "120px" },
          { text: "ID", value: "username", width: "240px" },  // ✅ Change value to user__username
          { text: "Full Name", value: "full_name", width: "240px" },  // ✅ Change value to user__username    
          { text: "Work Content", value: "content", width: "auto" },
          { text: "Notes", value: "notes", width: "auto" },
        ],
      };
    },
    async mounted() {
      this.fetchWorkLogs();
    },
    methods: {
      async fetchWorkLogs() {
        try {
          const token = localStorage.getItem("token");
          const response = await this.$http.get("admin/worklogs/", {
            headers: { Authorization: `Token ${token}` },
          });
          this.workLogs = response.data;
          this.filteredWorkLogs = response.data; // Initialize with full list
        } catch (error) {
          console.error("Error fetching work logs:", error);
        }
      },
      
      applyFilters() {
        this.filteredWorkLogs = this.workLogs.filter(log => {
          const matchesUsername =
            this.filterUsername === "" || log.username.toLowerCase().includes(this.filterUsername.toLowerCase());
          
          const logDate = new Date(log.date);
          const matchesStartDate = !this.startDate || logDate >= new Date(this.startDate);
          const matchesEndDate = !this.endDate || logDate <= new Date(this.endDate);

          return matchesUsername && matchesStartDate && matchesEndDate;
        });
      },
      async exportWorkLogs() {
        if (this.selectedLogs.length === 0) {
          alert("Please select at least one log to export.");
          return;
        }

        try {
          const token = localStorage.getItem("token");

          // ✅ Extract only IDs from selected work logs
          const selectedLogIds = this.selectedLogs.map(log => log.id);

          const response = await this.$http.post(
            "admin/worklogs/export/",
            { selectedLogs: selectedLogIds }, // ✅ Send only log IDs
            {
              headers: { Authorization: `Token ${token}` },
              responseType: "blob", // ✅ Ensures proper file download
            }
          );

          // ✅ Create & Trigger Download
          const blob = new Blob([response.data], { type: response.headers["content-type"] });
          const url = window.URL.createObjectURL(blob);
          const link = document.createElement("a");
          link.href = url;
          link.setAttribute("download", "worklogs.xlsx");
          document.body.appendChild(link);

          setTimeout(() => {
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);
          }, 100);

          console.log("✅ Work logs exported successfully!");
        } catch (error) {
          console.error("❌ Error exporting work logs:", error);
        }
      },
      async deleteSelectedLogs() {
        this.confirmDeleteDialog = false;  // ✅ Close the dialog
        if (!this.selectedLogs.length) return;

        try {
          const token = localStorage.getItem("token");

          // ✅ Extract only IDs from selected logs
          const selectedIds = this.selectedLogs.map(log => log.id);

          // ✅ Send DELETE requests for each selected log
          for (const logId of selectedIds) {
            await this.$http.delete(`/worklogs/${logId}/delete/`, {
              headers: { Authorization: `Token ${token}` },
            });
          }

          // ✅ Remove deleted logs from UI
          this.workLogs = this.workLogs.filter(log => !selectedIds.includes(log.id));
          this.selectedLogs = [];  // ✅ Clear selection after deletion
        } catch (error) {
          console.error("Error deleting work logs:", error);
        }
        await this.applyFilters();
      },
    }
  };
</script>
  