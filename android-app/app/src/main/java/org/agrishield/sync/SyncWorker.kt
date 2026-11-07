package org.agrishield.sync

import android.content.Context
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import org.agrishield.data.AgriShieldDatabase
import org.json.JSONArray
import org.json.JSONObject
import java.io.OutputStreamWriter
import java.net.HttpURLConnection
import java.net.URL

class SyncWorker(
    appContext: Context,
    workerParams: WorkerParameters
) : CoroutineWorker(appContext, workerParams) {

    override suspend fun doWork(): Result {
        val db = AgriShieldDatabase.getDatabase(applicationContext)
        val syncDao = db.syncQueueDao()
        val disasterDao = db.disasterReportDao()

        val pending = syncDao.getPendingMutations()
        if (pending.isEmpty()) {
            return Result.success()
        }

        return try {
            val endpoint = "http://10.0.2.2:8000/api/v1/sync/push" // Local emulator or server IP
            val url = URL(endpoint)
            val conn = url.openConnection() as HttpURLConnection
            conn.requestMethod = "POST"
            conn.setRequestProperty("Content-Type", "application/json")
            conn.doOutput = true
            conn.connectTimeout = 8000
            conn.readTimeout = 8000

            val payload = JSONObject()
            payload.put("device_id", "android_client_id")

            val mutationsArray = JSONArray()
            for (item in pending) {
                val m = JSONObject()
                m.put("client_mutation_id", item.clientMutationId)
                m.put("entity_type", item.entityType)
                m.put("operation", item.operation)
                m.put("payload", JSONObject(item.payloadJson))
                m.put("client_timestamp", "2026-11-07T12:00:00")
                mutationsArray.put(m)
            }
            payload.put("mutations", mutationsArray)

            val writer = OutputStreamWriter(conn.outputStream)
            writer.write(payload.toString())
            writer.flush()
            writer.close()

            if (conn.responseCode == 200) {
                val ackIds = pending.map { it.clientMutationId }
                syncDao.removeAcknowledged(ackIds)

                // Update local disaster reports status to SYNCED
                for (item in pending) {
                    if (item.entityType == "DISASTER_REPORT") {
                        disasterDao.updateSyncStatus(item.clientMutationId, "SYNCED")
                    }
                }
                Result.success()
            } else {
                Result.retry()
            }
        } catch (e: Exception) {
            Result.retry()
        }
    }
}
