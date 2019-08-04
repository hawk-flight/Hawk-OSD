/**
 * @file main.cpp
 * @author Dominik Gschwind
 * @brief
 * @version 0.1
 * @date 2019/08/03
 *
 * @copyright Copyright (c) 2019
 *
 */

#include <stm32g4xx.h>

/**
 * @brief Main function.
 */
int main() {
    RCC->AHB2ENR |= RCC_AHB2ENR_GPIOAEN;

    GPIOA->MODER = GPIO_MODER_MODE5_0;
    GPIOA->BSRR = GPIO_BSRR_BS5;

    uint32_t counter = 0;

    for (;;) {
        if (counter >= 2000000)
            counter = 0;
        
        if(!counter){
            if(GPIOA->ODR){
                GPIOA->ODR = 0;
            }
            else{
                GPIOA->ODR = GPIO_ODR_OD5;
            }
        }

        ++counter;
    }
}