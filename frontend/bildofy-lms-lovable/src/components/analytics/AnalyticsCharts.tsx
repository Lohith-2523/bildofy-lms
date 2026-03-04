import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export const SubjectPerformanceChart = ({ data }: { data: any[] }) => (
  <div className="h-64">
    <ResponsiveContainer width="100%" height="100%">
      <BarChart data={data}>
        <XAxis dataKey="subject" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="average_percentage" fill="#6366f1" />
      </BarChart>
    </ResponsiveContainer>
  </div>
);
