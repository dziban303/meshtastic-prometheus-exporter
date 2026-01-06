import logging
import json
from meshtastic_prometheus_exporter.metrics import *

logger = logging.getLogger("meshtastic_prometheus_exporter")


def on_meshtastic_position_app(packet, source_long_name, source_short_name):
    position = packet["decoded"].get("position", {})
    logger.debug(
        f"Received MeshPacket {packet['id']} with Position `{json.dumps(position, default=repr)}`"
    )

    source = packet["decoded"].get("source", packet["from"])
    position_attributes = {
        "source": source or "unknown",
        "source_long_name": source_long_name or "unknown",
        "source_short_name": source_short_name or "unknown",
    }

    if "satsInView" in position:
        logger.info(
            f"MeshPacket {packet['id']} has satsInView: {position['satsInView']}"
        )
        meshtastic_position_sats_in_view.set(
            position["satsInView"],
            attributes=position_attributes,
        )

    if "PDOP" in position:
        logger.info(f"MeshPacket {packet['id']} has PDOP: {position['PDOP']}")
        meshtastic_position_pdop.set(
            position["PDOP"],
            attributes=position_attributes,
        )

    if "HDOP" in position:
        logger.info(f"MeshPacket {packet['id']} has HDOP: {position['HDOP']}")
        meshtastic_position_hdop.set(
            position["HDOP"],
            attributes=position_attributes,
        )

    if "VDOP" in position:
        logger.info(f"MeshPacket {packet['id']} has VDOP: {position['VDOP']}")
        meshtastic_position_vdop.set(
            position["VDOP"],
            attributes=position_attributes,
        )
