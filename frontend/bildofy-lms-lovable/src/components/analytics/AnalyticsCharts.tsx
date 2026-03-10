import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from "recharts";

export const SubjectPerformanceChart = ({ data }: { data: any[] }) => (
  <div className="h-64">
    <ResponsiveContainer width="100%" height="100%">
      <BarChart data={data}>
        <XAxis dataKey="subject" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="average_percentage" fill="#6366f1" />
        <Bar dataKey="attendance_percentage" fill="#0f766e" />
      </BarChart>
    </ResponsiveContainer>
  </div>
);
