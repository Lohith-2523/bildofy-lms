export const StudentTable = ({ students }: { students: any[] }) => (
  <div className="overflow-auto">
    <table className="w-full text-sm border">
      <thead>
        <tr className="bg-muted">
          <th>Name</th>
          <th>Attempts</th>
          <th>Avg Score</th>
          <th>Avg %</th>
        </tr>
      </thead>
      <tbody>
        {students.map(s => (
          <tr key={s.student_id} className="border-t">
            <td>{s.name}</td>
            <td>{s.attempts}</td>
            <td>{s.average_score}</td>
            <td>{s.average_percentage}%</td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
);
