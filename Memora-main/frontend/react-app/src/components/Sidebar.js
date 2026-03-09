function Sidebar() {
  return (
    <div className="w-60 bg-gray-900 text-white p-4">
      <h2 className="text-lg font-bold mb-4">
        Memory Sources
      </h2>

      <div className="space-y-2">
        <div>📧 Emails</div>
        <div>📄 PDFs</div>
        <div>📊 CSV Files</div>
        <div>📝 Notes</div>
      </div>
    </div>
  );
}

export default Sidebar;