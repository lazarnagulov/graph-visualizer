const EventBus = {

    /** @type {Object<string, Function[]>} */
    events: {},


    /**
     * Subscribe to an event.
     * @param {string} event
     * @param {(data: any) => void} callback
     */
    on(event, callback) {
        (this.events[event] || []).push(callback);
    },


    /**
     * Emit an event.
     * @param {string} event
     * @param {any} data
     */
    emit(event, data) {
        (this.events[event] || []).forEach(callback => callback(data));
    },

    /**
     * Unsubscribe from an event.
     * @param {string} event
     * @param {(data: any) => void} callback
     */
    off(event, callback) {
        this.events[event] = (this.events[event] || []).filter(cb => cb !== callback);
    }
}

window.EventBus = EventBus;