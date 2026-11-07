package org.agrishield.model

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "local_farms")
data class LocalFarm(
    @PrimaryKey val id: String,
    val farmName: String,
    val district: String,
    val areaAcres: Double,
    val latitude: Double,
    val longitude: Double,
    val soilType: String,
    val irrigationType: String,
    val waterSource: String,
    val createdAtEpoch: Long = System.currentTimeMillis()
)

@Entity(tableName = "local_disaster_reports")
data class LocalDisasterReport(
    @PrimaryKey val id: String,
    val cropName: String,
    val disasterType: String,
    val incidentDateString: String,
    val affectedAreaAcres: Double,
    val damagePercentage: Double,
    val localPhotoPath: String?,
    val isWithin72h: Boolean,
    val hoursRemaining: Double,
    val sdrfReliefEstimateInr: Double,
    val syncStatus: String = "PENDING_SYNC", // PENDING_SYNC, SYNCED
    val createdAtEpoch: Long = System.currentTimeMillis()
)

@Entity(tableName = "sync_queue")
data class SyncQueueEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val clientMutationId: String,
    val entityType: String, // DISASTER_REPORT, PRODUCE_LISTING, FARM
    val operation: String,  // CREATE, UPDATE
    val payloadJson: String,
    val retryCount: Int = 0,
    val createdAtEpoch: Long = System.currentTimeMillis()
)
