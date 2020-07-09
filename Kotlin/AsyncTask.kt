// TODO: periodic function Template
private class RunTask(c: Context) : AsyncTask<Void, Void, String>() {
    private val context: Context = c

    override fun onPreExecute() {
        super.onPreExecute()
    }

    override fun doInBackground(vararg p0: Void?): String? {

        return null
    }

    override fun onPostExecute(result: String?) {
        super.onPostExecute(result)
    }

    override fun onCancelled(result: String?) {
        super.onCancelled(result)
    }
}


//CorontinScope
//GlobalScope.launch {}