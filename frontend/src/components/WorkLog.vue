<template>
  <v-container class="green-background fill-height d-flex align-center justify-center">
    <v-card class="pa-5" max-width="900">
      <h1 class="text-center">Work log of {{ username }}</h1>

      <v-data-table
        v-model="selectedLogs"
        :headers="headers"
        :items="workLogs"
        item-value="id"
        show-select
        class="elevation-1 mt-4"
        no-data-text="No work logs available"
      >
        <template v-slot:item.date="{ item }">
          <v-edit-dialog v-model="item.date" large persistent @save="updateWorkLog(item)">
            {{ item.date }}
            <v-text-field v-model="item.date" type="date" single-line dense></v-text-field>
          </v-edit-dialog>
        </template>

        <template #item.content="{ item }">
          <v-edit-dialog v-model="item.date" large persistent @save="updateWorkLog(item)">
            {{ item.content }}
            <template #input>
              <v-text-field v-model="item.content" label="Work Content" single-line dense></v-text-field>
            </template>
          </v-edit-dialog>
        </template>
        
        <template #item.notes="{ item }">
          <v-edit-dialog v-model="item.notes" large persistent @save="updateWorkLog(item)">
            {{ item.notes }}
            <template #input>
              <v-text-field v-model="item.notes" label="Notes" single-line dense></v-text-field>
            </template>
          </v-edit-dialog>
        </template>
      </v-data-table>

      <v-btn color="success" class="mt-4" @click="addPreviousDay">Add Previous Day</v-btn>
    </v-card>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      username: localStorage.getItem('username') || 'User',
      workLogs: [],
      selectedLogs: [],
      lastAddedDate: new Date(),
      headers: [
        { text: 'Date', value: 'date' },
        { text: 'Work Content', value: 'content' },
        { text: 'Notes', value: 'notes' },
      ],
    };
  },
  async mounted() {
    this.fetchWorkLogs();
  },
  methods: {
    async fetchWorkLogs() {
      try {
        const response = await this.$http.get('worklogs/', {
          headers: { Authorization: `Token ${localStorage.getItem('token')}` },
        });
        this.workLogs = response.data.sort((a, b) => new Date(b.date) - new Date(a.date));

        const today = new Date().toISOString().split('T')[0];
        if (!this.workLogs.some(log => log.date === today)) {
          this.workLogs.unshift({ id: null, date: today, content: '', notes: '' });
        }
      } catch (error) {
        console.error('Error fetching work logs:', error);
      }
    },
    async updateWorkLog(item) {
      try {
        if (item.id) {
          await this.$http.put(`worklogs/${item.id}/`, item, {
            headers: { Authorization: `Token ${localStorage.getItem('token')}` },
          });
        } else {
          await this.$http.post('worklogs/', item, {
            headers: { Authorization: `Token ${localStorage.getItem('token')}` },
          });
        }
        this.fetchWorkLogs();
      } catch (error) {
        console.error('Error updating work log:', error);
      }
    },
    addPreviousDay() {
      const previousDate = new Date(this.lastAddedDate);
      previousDate.setDate(previousDate.getDate() - 1);
      this.lastAddedDate = previousDate;

      this.workLogs.push({
        id: null,
        date: previousDate.toISOString().split('T')[0],
        content: '',
        notes: '',
      });
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
