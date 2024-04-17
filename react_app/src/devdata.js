import './style.css'

const Frame = ({ data }) => {
    return (
        <div className="panel">
        <h2 className="panel-title">Desarollado por: </h2>
        <div className="panel-content">
          {/* Aquí puedes mostrar tus datos */}
          <p>Marco Antonio Solis Gonzalez</p>
          <p>Carnet: 202003220</p>
        </div>
      </div>
    );
  }
  
  export default Frame;