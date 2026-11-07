package org.agrishield.data

import android.content.Context
import androidx.room.*
import org.agrishield.model.LocalFarm
import org.agrishield.model.LocalDisasterReport
import org.agrishield.model.SyncQueueEntity

@Dao
interface FarmDao {
    @Query("SELECT * FROM local_farms ORDER BY createdAtEpoch DESC")
    suspend fun getAllFarms(): List<LocalFarm>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertFarm(farm: LocalFarm)
}

@Dao
interface DisasterReportDao {
    @Query("SELECT * FROM local_disaster_reports ORDER BY createdAtEpoch DESC")
    suspend fun getAllReports(): List<LocalDisasterReport>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertReport(report: LocalDisasterReport)

    @Query("UPDATE local_disaster_reports SET syncStatus = :status WHERE id = :id")
    suspend fun updateSyncStatus(id: String, status: String)
}

@Dao
interface SyncQueueDao {
    @Query("SELECT * FROM sync_queue ORDER BY id ASC")
    suspend fun getPendingMutations(): List<SyncQueueEntity>

    @Insert
    suspend fun queueMutation(item: SyncQueueEntity)

    @Query("DELETE FROM sync_queue WHERE clientMutationId IN (:ids)")
    suspend fun removeAcknowledged(ids: List<String>)
}

@Database(
    entities = [LocalFarm::class, LocalDisasterReport::class, SyncQueueEntity::class],
    version = 1,
    exportSchema = false
)
abstract class AgriShieldDatabase : RoomDatabase() {
    abstract fun farmDao(): FarmDao
    abstract fun disasterReportDao(): DisasterReportDao
    abstract fun syncQueueDao(): SyncQueueDao

    companion object {
        @Volatile
        private var INSTANCE: AgriShieldDatabase? = null

        fun getDatabase(context: Context): AgriShieldDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    AgriShieldDatabase::class.java,
                    "agrishield_local.db"
                ).fallbackToDestructiveMigration().build()
                INSTANCE = instance
                instance
            }
        }
    }
}
