#ifndef FDC2214PROXSEN_EVM_REVA_FDC2214_H_
#define FDC2214PROXSEN_EVM_REVA_FDC2214_H_

#include "stdint.h"

#define FDC2214_SLAVE_ADDR_L			0x2A
#define FDC2214_SLAVE_ADDR_H			0x2B

/***********REGISTERS*********/
/*****************************/
#define	DATA_MSB_CH0_REG				0x00
#define DATA_LSB_CH0_REG				0x01
#define DATA_MSB_CH1_REG				0x02
#define DATA_LSB_CH1_REG				0x03
#define DATA_MSB_CH2_REG				0x04
#define DATA_LSB_CH2_REG				0x05
#define DATA_MSB_CH3_REG				0x06
#define DATA_LSB_CH3_REG				0x07
#define RCOUNT_CH0_REG					0x08
#define RCOUNT_CH1_REG					0x09
#define RCOUNT_CH2_REG					0x0A
#define RCOUNT_CH3_REG					0x0B
#define OFFSET_CH0_REG					0x0C
#define OFFSET_CH1_REG					0x0D
#define OFFSET_CH2_REG					0x0E
#define OFFSET_CH3_REG					0x0F
#define SETTLECOUNT_CH0_REG				0x10
#define SETTLECOUNT_CH1_REG				0x11
#define SETTLECOUNT_CH2_REG				0x12
#define SETTLECOUNT_CH3_REG				0x13
#define CLOCK_DIVIDERS_CH0_REG			0x14
#define CLOCK_DIVIDERS_CH1_REG			0x15
#define CLOCK_DIVIDERS_CH2_REG			0x16
#define CLOCK_DIVIDERS_CH3_REG			0x17
#define STATUS_REG						0x18
#define ERROR_CONFIG_REG				0x19
#define CONFIG_REG						0x1A
#define MUX_CONFIG_REG					0x1B
#define RESET_DEV_REG					0x1C
#define DRIVE_CURRENT_CH0_REG			0x1E
#define DRIVE_CURRENT_CH1_REG			0x1F
#define DRIVE_CURRENT_CH2_REG			0x20
#define DRIVE_CURRENT_CH3_REG			0x21
#define MAN_ID_REG						0x7E
#define DEV_ID_REG						0x7F

/**************DATA REGISTERs**************/
/******************************************/
#define CH0_ERR_WD						0x2000
#define CH0_ERR_AW						0x1000
#define DATA_MSB_CH0					0x0FFF
#define DATA_LSB_CH0					0xFFFF

#define CH1_ERR_WD						0x2000
#define CH1_ERR_AW						0x1000
#define DATA_MSB_CH1					0x0FFF
#define DATA_LSB_CH1					0xFFFF

#define CH2_ERR_WD						0x2000
#define CH2_ERR_AW						0x1000
#define DATA_MSB_CH2					0x0FFF
#define DATA_LSB_CH2					0xFFFF

#define CH3_ERR_WD						0x2000
#define CH3_ERR_AW						0x1000
#define DATA_MSB_CH3					0x0FFF
#define DATA_LSB_CH3					0xFFFF


/**************RCOUNT_CHx**********************/
/**********************************************/
#define CH0_RCOUNT						0xFFFF
#define CH1_RCOUNT						0xFFFF
#define CH2_RCOUNT						0xFFFF
#define CH3_RCOUNT						0xFFFF

/**************OFFSET_CHx**********************/
/**********************************************/
#define CH0_OFFSET						0xFFFF
#define CH1_OFFSET						0xFFFF
#define CH2_OFFSET						0xFFFF
#define CH3_OFFSET						0xFFFF


/***************STATUS REGISTER****************/
/**********************************************/
#define ERR_CHAN_0						0x0000
#define ERR_CHAN_1						0x1000
#define ERR_CHAN_2						0x2000
#define ERR_CHAN_3						0x3000
#define ERR_WD							0x0800
#define ERR_AHW							0x0400
#define ERR_ALW							0x0200
#define DRDY							0x0040
#define CH0_UNREADCONV					0x0008
#define CH1_UNREADCONV					0x0004
#define CH2_UNREADCONV					0x0002
#define CH3_UNREADCONV					0x0001

/***************ERROR CONFIG REGISTER**********/
/**********************************************/
#define WD_ERR2OUT						0x2000
#define AH_WARN2OUT						0x1000
#define AL_WARN2OUT						0x0800
#define WD_ERR2INT						0x0020
#define DRDY_2INT						0x0001


/***************CONFIG REGISTER****************/
/**********************************************/
#define ACTIVE_CHAN_0					0x0000
#define ACTIVE_CHAN_1					0x4000
#define ACTIVE_CHAN_2					0x8000
#define ACTIVE_CHAN_3					0xC000
#define SLEEP_MODE_EN					0x2000
#define SENSOR_ACTIVATE_SEL				0x0800
#define REF_CLK_SRC						0x0200
#define INTB_DIS						0x0080
#define HIGH_CURRENT_DRV				0x0040

/***************MUX CONFIG REGISTER************/
/**********************************************/
#define AUTOSCAN_EN						0x8000
#define RR_SEQUENCE0					0x0000
#define RR_SEQUENCE1					0x2000
#define RR_SEQUENCE2					0x4000
#define RR_SEQUENCE3					0x5000	// should be 0x6000 ?
#define DEGLITCH_1MHZ					0x0001
#define DEGLITCH_3P3MHZ					0x0004
#define DEGLITCH_10MHZ					0x0005
#define DEGLITCH_33MHZ					0x0007

/***************RESET DEV REGISTER*************/
/**********************************************/
#define RESET_DEV						0x8000
#define OUTPUT_GAIN_1					0x0000
#define OUTPUT_GAIN_4					0x0200
#define OUTPUT_GAIN_8					0x0400
#define OUTPUT_GAIN_16					0x0500

/***********CURRENT DRIVE SETTINGS************/
/*********************************************/
#define IDRIVE_0P016					0x0000
#define IDRIVE_0P018					0x0800
#define IDRIVE_0P021					0x1000
#define IDRIVE_0P025					0x1800
#define IDRIVE_0P028					0x2000
#define IDRIVE_0P033					0x2800
#define IDRIVE_0P038					0x3000
#define IDRIVE_0P044					0x3800
#define IDRIVE_0P052					0x4000
#define IDRIVE_0P060					0x4800
#define IDRIVE_0P069					0x5000
#define IDRIVE_0P081					0x5800
#define IDRIVE_0P093					0x6000
#define IDRIVE_0P108					0x6800
#define IDRIVE_0P126					0x7000
#define IDRIVE_0P146					0x7800
#define IDRIVE_0P169					0x8000
#define IDRIVE_0P196					0x8800
#define IDRIVE_0P228					0x9000
#define IDRIVE_0P264					0x9800
#define IDRIVE_0P307					0xA000
#define IDRIVE_0P356					0xA800
#define IDRIVE_0P413					0xB000
#define IDRIVE_0P479					0xB800
#define IDRIVE_0P555					0xC000
#define IDRIVE_0P644					0xC800
#define IDRIVE_0P747					0xD000
#define IDRIVE_0P867					0xD800
#define IDRIVE_1P006					0xE000
#define IDRIVE_1P167					0xE800
#define IDRIVE_1P354					0xF000
#define IDRIVE_1P571					0xF800


void FDC2214_init(void);//////////////////
void FDC2214_checkDevice(void);
void FDC2214_clockSetup(void);
void FDC2214_configINTB(void);
void FDC2214_enableINTB(void);
void FDC2214_disableINTB(void);
void FDC2214_proxSensorEnable(void);
void FDC2214_allChannelsEnable(void);
uint32_t FDC2214_readCh0(void);/////////////////
uint32_t FDC2214_readCh1(void);
uint32_t FDC2214_readCh2(void);
uint32_t FDC2214_readCh3(void);
void FDC2214_clearDRDY(void);
void FDC2214_sleep(void);
void FDC2214_wake(void);


#endif
