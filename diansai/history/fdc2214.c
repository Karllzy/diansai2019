#include "wiringPiI2C.h"
#include "fdc2214.h"
#include <stdint.h>
#include <stdio.h>
#include <unistd.h>

#define PROXIMITY_REFCOUNT			40000
#define BUTTON_REFCOUNT				1000
#define PROXIMITY_SETTLECOUNT       100
#define BUTTON_SETTLECOUNT			100

int i2cDevice;

void i2c_readByte(uint8_t address, uint8_t reg, uint8_t *pData)
{
    *pData = wiringPiI2CReadReg8(i2cDevice, reg);
    return;
}

void i2c_writeByte(uint8_t address, uint8_t reg, uint8_t data)
{
    wiringPiI2CWriteReg8(i2cDevice, reg, data);
    return;
}

void i2c_readWord(uint8_t SLAVE_ADDRESS, uint8_t reg, uint8_t *pData)
{
    *pData = wiringPiI2CReadReg16(i2cDevice, reg);
    return;
}

void i2c_writeWord(uint8_t address, uint8_t reg, uint16_t data)
{
    wiringPiI2CWriteReg16(i2cDevice, reg, data);
    return;
}

void FDC2214_init()
{
    i2cDevice = wiringPiI2CSetup(FDC2214_SLAVE_ADDR_L);

	//Set FDC_ADDR GPIO to 0 for SLAVE LOW ADDR
	//GPIO_setAsOutputPin(GPIO_PORT_P3, GPIO_PIN0);
	//GPIO_setOutputLowOnPin(GPIO_PORT_P3, GPIO_PIN0);

	//Disable SD pin
	//GPIO_setAsOutputPin(GPIO_PORT_P3, GPIO_PIN2);
	//GPIO_setOutputLowOnPin(GPIO_PORT_P3, GPIO_PIN2);

    //FDC2214_checkDevice();
	FDC2214_sleep();
	FDC2214_configINTB();
	FDC2214_clockSetup();
	FDC2214_allChannelsEnable();
	FDC2214_wake();
}

void FDC2214_checkDevice()
{
    uint8_t val[1] = {0};
    uint8_t readBackVal[2] = {0};
    uint16_t data = 0;

    i2c_readByte(FDC2214_SLAVE_ADDR_L, DEV_ID_REG, &val[0]);
    i2c_readWord(FDC2214_SLAVE_ADDR_L, MAN_ID_REG, &readBackVal[0]);

    data = ((uint16_t) (readBackVal[0] << 8) | readBackVal[1]);
}

void FDC2214_clockSetup()
{
	//REF COUNT
	i2c_writeWord(FDC2214_SLAVE_ADDR_L, RCOUNT_CH0_REG, (uint16_t)0x04D6);
	i2c_writeWord(FDC2214_SLAVE_ADDR_L, RCOUNT_CH1_REG, (uint16_t)0x04D6);
	i2c_writeWord(FDC2214_SLAVE_ADDR_L, RCOUNT_CH2_REG, (uint16_t)0x04D6);
    i2c_writeWord(FDC2214_SLAVE_ADDR_L, RCOUNT_CH3_REG, (uint16_t)0x04D6);

    i2c_writeWord(FDC2214_SLAVE_ADDR_L, OFFSET_CH0_REG, (uint16_t)0x0F00);
	i2c_writeWord(FDC2214_SLAVE_ADDR_L, OFFSET_CH1_REG, (uint16_t)0x0F00);
	i2c_writeWord(FDC2214_SLAVE_ADDR_L, OFFSET_CH2_REG, (uint16_t)0x0F00);
    i2c_writeWord(FDC2214_SLAVE_ADDR_L, OFFSET_CH3_REG, (uint16_t)0x0F00);

	//Settle Count
	i2c_writeWord(FDC2214_SLAVE_ADDR_L, SETTLECOUNT_CH0_REG, (uint16_t)0x000A);
	i2c_writeWord(FDC2214_SLAVE_ADDR_L, SETTLECOUNT_CH1_REG, (uint16_t)0x000A);
	i2c_writeWord(FDC2214_SLAVE_ADDR_L, SETTLECOUNT_CH2_REG, (uint16_t)0x000A);
	i2c_writeWord(FDC2214_SLAVE_ADDR_L, SETTLECOUNT_CH3_REG, (uint16_t)0x000A);
}

void FDC2214_configINTB()
{
	//GPIO_setAsInputPin(GPIO_PORT_P3, GPIO_PIN1);
	return;
}

void FDC2214_enableINTB()
{
	uint8_t readBackVal[2] = {0};
	uint16_t data = 0;

	//Enable GPIO interrupt pin
	//GPIO_enableInterrupt(GPIO_PORT_P3, GPIO_PIN1);
	//GPIO_selectInterruptEdge(GPIO_PORT_P3, GPIO_PIN1, GPIO_HIGH_TO_LOW_TRANSITION);

	//Select INTB pin enable on FDC2214
	i2c_readWord(FDC2214_SLAVE_ADDR_L, CONFIG_REG, &readBackVal[0]);
	data = (readBackVal[0] << 8) | readBackVal[1];
	data = data & ~(INTB_DIS);
	i2c_writeWord(FDC2214_SLAVE_ADDR_L, CONFIG_REG, data);

	//Configure ERROR_CONFIG for DRDY_2INT
	i2c_readWord(FDC2214_SLAVE_ADDR_L, ERROR_CONFIG_REG, &readBackVal[0]);
	data = (readBackVal[0] << 8) | readBackVal[1];
	data = data | DRDY_2INT;
	i2c_writeWord(FDC2214_SLAVE_ADDR_L, ERROR_CONFIG_REG, data);
}

void FDC2214_disableINTB()
{
	//GPIO_disableInterrupt(GPIO_PORT_P3, GPIO_PIN1);
	return;
}

void FDC2214_allChannelsEnable()
{
	//Need to wake up device after this function call
	uint16_t configData = 0;
	uint16_t muxConfigData = 0;

	//Select single channel measurement and configure
	configData = (SLEEP_MODE_EN | SENSOR_ACTIVATE_SEL | REF_CLK_SRC
					& ~(INTB_DIS | HIGH_CURRENT_DRV));
	configData = (configData | (1<<12) | (1<<10));		//Set reserve bits to 1 per datasheet

	i2c_writeWord(FDC2214_SLAVE_ADDR_L, CONFIG_REG, configData);

	//Select measurement sequence
	muxConfigData = (AUTOSCAN_EN | RR_SEQUENCE0 | DEGLITCH_10MHZ);
	muxConfigData = (muxConfigData | (1<<9) | (1<<3));	//set reserve bits to 1 per datasheet

	i2c_writeWord(FDC2214_SLAVE_ADDR_L, MUX_CONFIG_REG, muxConfigData);

    //i2c_writeWord(FDC2214_SLAVE_ADDR_L, MUX_CONFIG_REG, (uint16_t)0xC20D);
	//Adjust drive current for better sensitivity
	i2c_writeWord(FDC2214_SLAVE_ADDR_L, DRIVE_CURRENT_CH0_REG, IDRIVE_0P228);
	i2c_writeWord(FDC2214_SLAVE_ADDR_L, DRIVE_CURRENT_CH1_REG, IDRIVE_0P228);
	i2c_writeWord(FDC2214_SLAVE_ADDR_L, DRIVE_CURRENT_CH2_REG, IDRIVE_0P228);
	i2c_writeWord(FDC2214_SLAVE_ADDR_L, DRIVE_CURRENT_CH3_REG, IDRIVE_0P228);
	usleep(10000);
}

uint32_t FDC2214_readCh0(void)
{
	uint8_t readBackVal[2] = {0};
	uint16_t dataMSB = 0;
	uint16_t dataLSB = 0;

	//CH0 measurement
	i2c_readWord(FDC2214_SLAVE_ADDR_L, DATA_MSB_CH0_REG, &readBackVal[0]);	//MSB
	dataMSB = (((uint16_t) (readBackVal[0] << 8)) | readBackVal[1]) & ~(0xF000);			//Mask the upper 4 bits

	i2c_readWord(FDC2214_SLAVE_ADDR_L, DATA_LSB_CH0_REG, &readBackVal[0]);	//LSB
	dataLSB = (((uint16_t) readBackVal[0] << 8)) | readBackVal[1];			//Mask the upper 4 bits

	return ( (((uint32_t) dataMSB) << 16) | dataLSB);
}

uint32_t FDC2214_readCh1(void)
{
	uint8_t readBackVal[2] = {0};
	uint16_t dataMSB = 0;
	uint16_t dataLSB = 0;

	//CH0 measurement (Button 1)
	i2c_readWord(FDC2214_SLAVE_ADDR_L, DATA_MSB_CH1_REG, &readBackVal[0]);	//MSB
	dataMSB = (((uint16_t) (readBackVal[0] << 8)) | readBackVal[1]) & ~(0xF000);			//Mask the upper 4 bits
	i2c_readWord(FDC2214_SLAVE_ADDR_L, DATA_LSB_CH1_REG, &readBackVal[0]);	//LSB
	dataLSB = (((uint16_t) readBackVal[0] << 8)) | readBackVal[1];						//Mask the upper 4 bits

	return ((((uint32_t) dataMSB) << 16) | dataLSB);
}

uint32_t FDC2214_readCh2(void)
{
	uint8_t readBackVal[2] = {0};
	uint16_t dataMSB = 0;
	uint16_t dataLSB = 0;

	//CH1 measurement (Button 2)
	i2c_readWord(FDC2214_SLAVE_ADDR_L, DATA_MSB_CH2_REG, &readBackVal[0]);	//MSB
	dataMSB = (((uint16_t) (readBackVal[0] << 8)) | readBackVal[1]) & ~(0xF000);			//Mask the upper 4 bits
	i2c_readWord(FDC2214_SLAVE_ADDR_L, DATA_LSB_CH2_REG, &readBackVal[0]);	//LSB
	dataLSB = (((uint16_t) readBackVal[0] << 8)) | readBackVal[1];						//Mask the upper 4 bits

	return ((((uint32_t) dataMSB) << 16) | dataLSB);
}

uint32_t FDC2214_readCh3(void)
{
	uint8_t readBackVal[2] = {0};
	uint16_t dataMSB = 0;
	uint16_t dataLSB = 0;

	//CH1 measurement (Button 2)
	i2c_readWord(FDC2214_SLAVE_ADDR_L, DATA_MSB_CH3_REG, &readBackVal[0]);	//MSB
	dataMSB = (((uint16_t) (readBackVal[0] << 8)) | readBackVal[1]) & ~(0xF000);			//Mask the upper 4 bits
	i2c_readWord(FDC2214_SLAVE_ADDR_L, DATA_LSB_CH3_REG, &readBackVal[0]);	//LSB
	dataLSB = (((uint16_t) readBackVal[0] << 8)) | readBackVal[1];						//Mask the upper 4 bits

	return ((((uint32_t) dataMSB) << 16) | dataLSB);
}

void FDC2214_clearDRDY(void)
{
	//Clearing the DRDY bit when INTB interrupt occurs by reading STATUS reg
	uint8_t readBackVal[2] = {0};

	i2c_readWord(FDC2214_SLAVE_ADDR_L, STATUS_REG, &readBackVal[0]);
}

void FDC2214_sleep(void)
{
	uint8_t readBackVal[2] = {0};
	uint16_t data = 0;

	//Only change SLEEP MODE BIT
	i2c_readWord(FDC2214_SLAVE_ADDR_L, CONFIG_REG, &readBackVal[0]);
	data = (readBackVal[0] << 8) | readBackVal[1];

	data = (data | SLEEP_MODE_EN);		//ENABLE SLEEP MODE

	i2c_writeWord(FDC2214_SLAVE_ADDR_L, CONFIG_REG, data);
}

void FDC2214_wake(void)
{
	uint8_t readBackVal[2] = {0};
	uint16_t data = 0;

	//Only change SLEEP MODE BIT
	i2c_readWord(FDC2214_SLAVE_ADDR_L, CONFIG_REG, &readBackVal[0]);
	data = (readBackVal[0] << 8) | readBackVal[1];

	data = (data & (~SLEEP_MODE_EN));	//DISABLE SLEEP MODE

	i2c_writeWord(FDC2214_SLAVE_ADDR_L, CONFIG_REG, data);
}
/*
int main()
{
    FDC2214_init();
    FDC2214_allChannelsEnable();
    while (1)
    {
        uint32_t ch0Val = FDC2214_readCh0();
        uint32_t ch1Val = FDC2214_readCh1();
        uint32_t ch2Val = FDC2214_readCh2();
        usleep(200000);
        uint32_t ch3Val = FDC2214_readCh3();
        printf("CH0=%d,CH1=%d,CH2=%d,CH3=%d\n",
        ch0Val, ch1Val, ch2Val, ch3Val);
    }
    return 0;
}
*/
