<template>
  <v-container fluid>
    <v-card>
      <v-card-title>
        All Work Logs
        <v-spacer></v-spacer>

        <!-- ✅ Export Button -->
        <v-btn
          color="success"
          :disabled="selectedLogs.length === 0"
          @click="exportWorkLogs"
        >
          Export to Excel
        </v-btn>
      </v-card-title>
      <v-data-table
        v-model="selectedLogs"
        :headers="headers"
        :items="workLogs"
        item-value="id"
        class="elevation-1 mt-4"
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
  </v-container>
</template>

<style scoped>
/* Ensures multi-line text wraps properly */
.multiline-text {
  white-space: pre-wrap;  /* Keeps line breaks */
  word-wrap: break-word;  /* Prevents overflow */
  max-width: 100%;
}
</style>
  
  <script>
  /* eslint-disable no-unused-vars */
  export default {
    data() {
      return {
        selectedLogs: [],  // Store selected log IDs
        workLogs: [],
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
      try {
        const token = localStorage.getItem('token');
        const response = await this.$http.get('admin/worklogs/', {
            headers: { Authorization: `Token ${token}` }
        });
        this.workLogs = response.data;
      } catch (error) {
        console.error('Error fetching work logs:', error);
      }
    },
    methods: {
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
    }
  };
  </script>
  